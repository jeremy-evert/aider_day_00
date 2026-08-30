import random

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
        prize    = random.choice(DOORS)
        player   = random.choice(DOORS)
        host     = get_host_door(prize, player)
        switched = next(d for d in DOORS if d != player and d != host)

        if player == prize:
            stay_wins += 1
        if switched == prize:
            switch_wins += 1

    print(f"Trials:        {trials}")
    print(f"Always stay:   {stay_wins}/{trials}  ({stay_wins / trials:.1%})")
    print(f"Always switch: {switch_wins}/{trials}  ({switch_wins / trials:.1%})")


# --- main ---
print("=== Monty Hall ===")
print("  1. Play one game")
print("  2. Run a simulation")
print()

while True:
    mode = input("Choose 1 or 2: ").strip()
    if mode in ("1", "2"):
        break
    print("Please type 1 or 2.")

if mode == "1":
    play_one_round()
else:
    while True:
        raw = input("How many trials? ").strip()
        try:
            trials = int(raw)
            if trials > 0:
                break
        except ValueError:
            pass
        print("Please enter a positive whole number.")
    simulate(trials)
