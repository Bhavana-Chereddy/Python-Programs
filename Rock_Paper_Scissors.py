# 1. Assign variables to both the players to keep score after each game. Start from 0.
# 2. Ask for the player names - player_1 & player_2
# 3. Ask for the number of games that are to be played - number_of_games
# 4. Run a loop for the number_of_games
#   a. Ask for inputs from player_1 & player_2. String inputs.
#   b. Determine winner for each game
# 5. Print the winner of the game. Compare both variables from step 1. Display name of player with greater value.
import random

def printScores(p1name, p2name, games_won_p1, games_won_p2):
    print('Scores so far...')
    print(p1name + ":" + str(games_won_p1))
    print(p2name + ":" + str(games_won_p2))
    print('===============================================')

def playRockPaperScissors():
    dictionary = {
        1: "ROCK",
        2: "PAPER",
        3: "SCISSORS"
    }

    games_won_by_player_1 = 0
    games_won_by_player_2 = 0

    player_1_name = input("Player 1, enter your name here:")
    player_2_name = input("Player 2, enter your name here:")

    while True:
        try:
            number_of_games = int(input("Enter the number of games you want to play:"))
            break
        except:
            print("Number of games must be an integer.")
            continue
    i = 1
    while i <= number_of_games:
        print('GAME #:' + str(i))

        try:
            player_1_input = int(input(player_1_name + ": Enter 1 for Rock, 2 for Paper or 3 for Scissors?"))
            player_2_input = int(input(player_2_name + ": Enter 1 for Rock, 2 for Paper or 3 for Scissors?"))

            #player_1_input = random.randint(1, 3) - alternative to collect input
            #player_2_input = random.randint(1, 3) - alternative to collect input

            if player_1_input < 1 or player_1_input > 3 or player_2_input < 1 or player_2_input > 3:
                raise Exception("Must enter 1, 2 or 3 for Rock, Paper or Scissors")

            i += 1
        except:
            print("Must enter 1, 2 or 3 for Rock, Paper or Scissors")
            continue

        # Determining the winner
        if player_1_input == player_2_input:
            print("It's a draw!")
            printScores(player_1_name, player_2_name, games_won_by_player_1, games_won_by_player_2)
            continue

        if player_1_input == 1 and player_2_input == 3:
            games_won_by_player_1 += 1
            printScores(player_1_name, player_2_name, games_won_by_player_1, games_won_by_player_2)
            continue

        if player_1_input == 3 and player_2_input == 1:
            games_won_by_player_2 += 1
            printScores(player_1_name, player_2_name, games_won_by_player_1, games_won_by_player_2)
            continue

        if player_1_input > player_2_input:
            games_won_by_player_1 += 1
        else:
            games_won_by_player_2 += 1
        printScores(player_1_name, player_2_name, games_won_by_player_1, games_won_by_player_2)

    if games_won_by_player_1 > games_won_by_player_2:
        print(player_1_name, "you are the winner!")
    elif games_won_by_player_1 < games_won_by_player_2:
        print(player_2_name, "you are the winner!")
    else:
        print("It's a draw! No one wins.")

playRockPaperScissors()
