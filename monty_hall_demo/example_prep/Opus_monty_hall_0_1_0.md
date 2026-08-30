import random

DOORS = [1, 2, 3]

def get_host_door(prize, player):
    """Pick a door the host can safely open — not the prize, not the player's."""
    options = [d for d in DOORS if d != prize and d != player]
    return random.choice(options)

def play():
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

play()