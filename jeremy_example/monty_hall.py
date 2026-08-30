import random

doors = [1, 2, 3]
prize_door = random.choice(doors)

def get_player_choice():
    while True:
        try:
            choice = int(input("Enter a door (1, 2, or 3): "))
            if choice in doors:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

player_choice = get_player_choice()
print(f"You chose door {player_choice}.")
