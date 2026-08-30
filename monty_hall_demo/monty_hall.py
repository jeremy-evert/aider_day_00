"""Small, dependency-free Monty Hall game and simulation."""

import argparse
import html
import math
import random
from collections.abc import Callable, Sequence
from datetime import datetime
from pathlib import Path


DOORS = (1, 2, 3)
SWITCH_LABEL = "switch"


def _random_source(rng=None):
    """Use the module-level generator unless a test supplies one."""
    return random if rng is None else rng


def choose_host_door(prize_door: int, player_door: int, rng=None) -> int:
    """Return a losing door the host can safely reveal."""
    if prize_door not in DOORS or player_door not in DOORS:
        raise ValueError("door numbers must be 1, 2, or 3")
    choices = [door for door in DOORS if door != prize_door and door != player_door]
    return _random_source(rng).choice(choices)


def remaining_closed_door(player_door: int, revealed_door: int) -> int:
    """Return the only door left closed after the host reveals one door."""
    if player_door not in DOORS or revealed_door not in DOORS:
        raise ValueError("door numbers must be 1, 2, or 3")
    if player_door == revealed_door:
        raise ValueError("the host cannot reveal the player's door")
    return next(door for door in DOORS if door not in (player_door, revealed_door))


def play_round(player_door: int, switch: bool, rng=None) -> tuple[bool, int, int, int]:
    """Run one round and return win, prize, revealed, and final door."""
    if player_door not in DOORS:
        raise ValueError("door numbers must be 1, 2, or 3")
    source = _random_source(rng)
    prize_door = source.choice(DOORS)
    revealed_door = choose_host_door(prize_door, player_door, source)
    final_door = (
        remaining_closed_door(player_door, revealed_door)
        if switch
        else player_door
    )
    return final_door == prize_door, prize_door, revealed_door, final_door


def simulate(trials: int, rng=None) -> tuple[int, int]:
    """Compare always-stay and always-switch over the same trial setups."""
    if trials <= 0:
        raise ValueError("trials must be a positive integer")

    source = _random_source(rng)
    stay_wins = 0
    switch_wins = 0
    for _ in range(trials):
        prize_door = source.choice(DOORS)
        player_door = source.choice(DOORS)
        revealed_door = choose_host_door(prize_door, player_door, source)
        switched_door = remaining_closed_door(player_door, revealed_door)
        stay_wins += int(player_door == prize_door)
        switch_wins += int(switched_door == prize_door)
    return stay_wins, switch_wins


def run_trials(trials: int, rng=None) -> dict[str, object]:
    """Return reproducible strategy and per-door counts for a report."""
    if trials <= 0:
        raise ValueError("trials must be a positive integer")
    source = _random_source(rng)
    stay_wins = switch_wins = 0
    prize_count = {door: 0 for door in DOORS}
    first_pick_count = {door: 0 for door in DOORS}
    for _ in range(trials):
        prize = source.choice(DOORS)
        player = source.choice(DOORS)
        revealed = choose_host_door(prize, player, source)
        switched = remaining_closed_door(player, revealed)
        prize_count[prize] += 1
        first_pick_count[player] += 1
        stay_wins += int(player == prize)
        switch_wins += int(switched == prize)
    return {
        "trials": trials,
        "stay_wins": stay_wins,
        "switch_wins": switch_wins,
        "prize_count": prize_count,
        "first_pick_count": first_pick_count,
        "margin": 1.96 * math.sqrt(0.25 / trials),
    }


def _write_html(path: str, stats: dict[str, object], timestamp: str | None) -> None:
    trials = int(stats["trials"])
    stay = int(stats["stay_wins"])
    switch = int(stats["switch_wins"])
    stamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")
    body = "\n".join(
        f"<li>Door {door}: {stats['prize_count'][door]:,}/{trials:,}</li>"
        for door in DOORS
    )
    Path(path).write_text(
        "<!DOCTYPE html>\n<html lang='en'><meta charset='utf-8'>"
        f"<title>Monty Hall — {trials:,} trials</title><body>"
        f"<h1>Monty Hall simulation</h1><p>Generated {html.escape(stamp)}</p>"
        f"<p>Always stay: {stay:,}/{trials:,} ({stay / trials:.1%})</p>"
        f"<p>Always switch: {switch:,}/{trials:,} ({switch / trials:.1%})</p>"
        f"<p>95% uncertainty margin: +/- {float(stats['margin']):.2%}</p>"
        f"<h2>Prize placement</h2><ul>{body}</ul>"
        "<h2>Three course lenses</h2><p>CS1: functions and tests. "
        "Discrete Structures: a constrained sample space. Computer "
        "Architecture: repeated state transitions cost time.</p></body></html>\n",
        encoding="utf-8",
    )


def _ask_for_door(input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> int:
    while True:
        raw = input_fn("Choose a door (1, 2, or 3): ").strip()
        try:
            door = int(raw)
        except ValueError:
            door = 0
        if door in DOORS:
            return door
        output_fn("Invalid door. Choose 1, 2, or 3.")


def _ask_to_switch(input_fn: Callable[[str], str], output_fn: Callable[[str], None]) -> bool:
    while True:
        answer = input_fn("Stay with your door or switch? (stay/switch): ").strip().lower()
        if answer in {"stay", "s"}:
            return False
        if answer in {"switch", "change", "c"}:
            return True
        output_fn("Invalid choice. Type stay or switch.")


def play_game(
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    rng=None,
) -> bool:
    """Run the interactive three-door game and return whether the player won."""
    player_door = _ask_for_door(input_fn, output_fn)
    source = _random_source(rng)
    prize_door = source.choice(DOORS)
    revealed_door = choose_host_door(prize_door, player_door, source)
    output_fn(f"The host opens door {revealed_door}, revealing a goat.")
    switch = _ask_to_switch(input_fn, output_fn)
    final_door = remaining_closed_door(player_door, revealed_door) if switch else player_door
    won = final_door == prize_door
    result = "win" if won else "lose"
    output_fn(f"You chose door {final_door}. The prize was behind door {prize_door}.")
    output_fn(f"Result: {result}.")
    return won


def _print_simulation(
    trials: int,
    output_fn: Callable[[str], None] = print,
    stats: dict[str, object] | None = None,
) -> None:
    if stats is None:
        stay_wins, switch_wins = simulate(trials)
    else:
        stay_wins = int(stats["stay_wins"])
        switch_wins = int(stats["switch_wins"])
    output_fn(f"Trials: {trials}")
    output_fn(f"Always stay:   {stay_wins}/{trials} ({stay_wins / trials:.1%})")
    output_fn(f"Always switch: {switch_wins}/{trials} ({switch_wins / trials:.1%})")


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Play or simulate the Monty Hall problem.")
    parser.add_argument("--simulate", type=int, metavar="TRIALS", help="run a trial comparison")
    parser.add_argument("--seed", type=int, help="seed the random source for replay")
    parser.add_argument("--html", metavar="PATH", help="write a standalone HTML report")
    parser.add_argument("--timestamp", help="fixed report timestamp for deterministic replay")
    args = parser.parse_args(argv)
    if args.seed is not None:
        random.seed(args.seed)
    if args.html and args.simulate is None:
        parser.error("--html requires --simulate")
    if args.simulate is not None:
        if args.simulate <= 0:
            parser.error("--simulate requires a positive trial count")
        stats = run_trials(args.simulate)
        _print_simulation(args.simulate, stats=stats)
        if args.html:
            _write_html(args.html, stats, args.timestamp)
        return
    if args.seed is not None or args.timestamp:
        parser.error("--seed and --timestamp require --simulate")
    play_game()


if __name__ == "__main__":
    main()
