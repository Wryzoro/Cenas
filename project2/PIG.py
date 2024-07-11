import random

def roll():
    min_value = 1
    max_value = 6
    roll = random.randint(min_value, max_value)
    return roll

while True:
    players_input = input("How many players are playing (1-4)? ")
    if players_input.isdigit():
        players = int(players_input)
        if 1 <= players <= 4:
            break
        else:
            print("Must be between 1 and 4 players.")
    else:
        print("Invalid input. Please enter a number.")

max_score = 50
players_scores = [0 for _ in range(players)]


while max(players_scores) < max_score:

    for player_idx in range(players):
        current_score = 0
            
        while True:
            should_roll = input("Do you want to roll the dice? (y): ")
            if should_roll.lower() != "y":
                break

            value = roll()
            if value == 0:
                print("You rolled a 1. Turn done!")
                break
            else:
                current_score += value
                print(f"You rolled a {value}.")

            print("Your current score is:", current_score)

        players_scores[player_idx] += current_score
        print("Your total score is:", players_scores[player_idx])

