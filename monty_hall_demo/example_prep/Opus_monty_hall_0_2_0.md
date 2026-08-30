import random
import sys

DOORS = [1, 2, 3]


def get_host_door(prize, player):
    """Pick a door the host can safely open — not the prize, not the player's."""
    options = [d for d in DOORS if d != prize and d != player]
    return random.choice(options)


def play_one_round():
    prize = random.choice(DOORS)

    # Player picks a door
    while True:
        raw = input("Pick a door (1, 2, or 3): ").strip()
        if raw in ("1", "2", "3"):
            player = int(raw)
            break
        print("Please pick 1, 2, or 3.")

    # Host opens a losing door
    host = get_host_door(prize, player)
    print(f"The host opens door {host} — there's a goat!")

    # Stay or switch?
    while True:
        answer = input("Stay or switch? ").strip().lower()
        if answer in ("stay", "switch"):
            break
        print("Type 'stay' or 'switch'.")

    if answer == "switch":
        player = next(d for d in DOORS if d != player and d != host)

    # Result
    if player == prize:
        print(f"Door {player}: PRIZE! You win! 🎉")
    else:
        print(f"Door {player}: goat. Prize was behind door {prize}. You lose.")


def simulate(trials):
    stay_wins = 0
    switch_wins = 0

    for _ in range(trials):
        prize  = random.choice(DOORS)
        player = random.choice(DOORS)
        host   = get_host_door(prize, player)
        switched = next(d for d in DOORS if d != player and d != host)

        if player == prize:
            stay_wins += 1
        if switched == prize:
            switch_wins += 1

    print(f"Trials:        {trials}")
    print(f"Always stay:   {stay_wins}/{trials}  ({stay_wins / trials:.1%})")
    print(f"Always switch: {switch_wins}/{trials}  ({switch_wins / trials:.1%})")


# --- main ---
if len(sys.argv) == 3 and sys.argv[1] == "--simulate":
    try:
        trials = int(sys.argv[2])
        if trials <= 0:
            raise ValueError
    except ValueError:
        print("Usage: python game.py --simulate <positive whole number>")
        sys.exit(1)
    simulate(trials)
else:
    play_one_round()
