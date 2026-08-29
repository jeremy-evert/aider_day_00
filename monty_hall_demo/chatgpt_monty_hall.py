"""Small, dependency-free Monty Hall game and simulation."""

import argparse
import random
from collections.abc import Callable, Sequence

DOORS = (1, 2, 3)


def _random_source(rng=None):
    """Use the module-level generator unless a test supplies one."""
    return random if rng is None else rng


def choose_host_door(prize_door: int, player_door: int, rng=None) -> int:
    """Return a losing door the host can safely reveal."""
    if prize_door not in DOORS or player_door not in DOORS:
        raise ValueError("door numbers must be 1, 2, or 3")
    choices = [
        door
        for door in DOORS
        if door != prize_door and door != player_door
    ]
    return _random_source(rng).choice(choices)


def remaining_closed_door(player_door: int, revealed_door: int) -> int:
    """Return the only door left closed after the host reveals one door."""
    if player_door not in DOORS or revealed_door not in DOORS:
        raise ValueError("door numbers must be 1, 2, or 3")
    if player_door == revealed_door:
        raise ValueError("the host cannot reveal the player's door")
    return next(
        door for door in DOORS
        if door not in (player_door, revealed_door)
    )


def play_round(
    player_door: int,
    switch: bool,
    rng=None,
) -> tuple[bool, int, int, int]:
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


def _ask_for_door(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> int:
    """Prompt until the player enters door 1, 2, or 3."""
    while True:
        raw = input_fn("Choose a door (1, 2, or 3): ").strip()
        try:
            door = int(raw)
        except ValueError:
            door = 0
        if door in DOORS:
            return door
        output_fn("Invalid door. Choose 1, 2, or 3.")


def _ask_to_switch(
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> bool:
    """Prompt until the player chooses to stay or switch."""
    while True:
        answer = input_fn(
            "Stay with your door or switch? (stay/switch): "
        ).strip().lower()
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
    final_door = (
        remaining_closed_door(player_door, revealed_door)
        if switch
        else player_door
    )
    won = final_door == prize_door
    result = "win" if won else "lose"
    output_fn(
        f"You chose door {final_door}. "
        f"The prize was behind door {prize_door}."
    )
    output_fn(f"Result: {result}.")
    return won


def _print_simulation(
    trials: int,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Print stay and switch results for the requested number of trials."""
    stay_wins, switch_wins = simulate(trials)
    output_fn(f"Trials: {trials}")
    output_fn(
        f"Always stay:   {stay_wins}/{trials} "
        f"({stay_wins / trials:.1%})"
    )
    output_fn(
        f"Always switch: {switch_wins}/{trials} "
        f"({switch_wins / trials:.1%})"
    )


def main(argv: Sequence[str] | None = None) -> None:
    """Run the interactive game or simulation mode."""
    parser = argparse.ArgumentParser(
        description="Play or simulate the Monty Hall problem."
    )
    parser.add_argument(
        "--simulate",
        type=int,
        metavar="TRIALS",
        help="run a stay-versus-switch trial comparison",
    )
    args = parser.parse_args(argv)

    if args.simulate is not None:
        if args.simulate <= 0:
            parser.error("--simulate requires a positive trial count")
        _print_simulation(args.simulate)
        return

    play_game()


if __name__ == "__main__":
    main()
