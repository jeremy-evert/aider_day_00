import random

DOORS = [1, 2, 3]

def place_prize_and_goats():
    prize_door = random.choice(DOORS)
    goats = [door for door in DOORS if door != prize_door]
    return prize_door, goats

def get_player_choice():
    while True:
        try:
            player_choice = int(input("Choose a door (1, 2, or 3): "))
            if player_choice not in DOORS:
                raise ValueError
            return player_choice
        except ValueError:
            print("Invalid input. Please choose a valid door number.")

def reveal_losing_door(prize_door, player_choice):
    goats = [door for door in DOORS if door != prize_door and door != player_choice]
    revealed_door = random.choice(goats)
    return revealed_door

def ask_stay_or_switch():
    while True:
        try:
            stay_or_switch = input("Do you want to stay or switch? (stay/switch): ").strip().lower()
            if stay_or_switch not in ['stay', 'switch']:
                raise ValueError
            return stay_or_switch
        except ValueError:
            print("Invalid input. Please choose 'stay' or 'switch'.")

def reveal_selected_door(player_choice, stay_or_switch, revealed_door):
    if stay_or_switch == 'stay':
        selected_door = player_choice
    else:
        selected_door = revealed_door
    return selected_door

def reveal_result(prize_door, selected_door):
    if prize_door == selected_door:
        print("Congratulations! You won the prize!")
    else:
        print("Sorry, you lost. The prize was behind door", prize_door)

def main():
    prize_door, goats = place_prize_and_goats()
    player_choice = get_player_choice()
    revealed_door = reveal_losing_door(prize_door, player_choice)
    stay_or_switch = ask_stay_or_switch()
    selected_door = reveal_selected_door(player_choice, stay_or_switch, revealed_door)
    reveal_result(prize_door, selected_door)

if __name__ == "__main__":
    main()
