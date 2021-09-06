# 1. create 2 variables player_1 & player_2 names
# 2. Display Player_1 is X & player_2 is O
# 3. X and O take turns alternatively
#   - Use dictionary to print the board. print after every turn.
#   - All rows are either X's or O's
#   - All columns are either X's or O's
#   - Diagnols are either X's or O's
#4. print out the winner of the game

def print_board(board):
    print("TIC TAC TOE")
    print(" " + board[1] + "|" + board[2] + "|" + board[3])
    print(" --+-+--")
    print("  " + board[4] + "|" + board[5] + "|" + board[6])
    print(" --+-+--")
    print("  " + board[7] + "|" + board[8] + "|" + board[9])

def determine_winner(board):
    if board[1] == board[2] and board[2] == board[3]:
        return True
    elif board[4] == board[5] and board[5] == board[6]:
        return True
    elif board[7] == board[8] and board[8] == board[9]:
        return True
    elif board[1] == board[4] and board[4] == board[7]:
        return True
    elif board[2] == board[5] and board[5] == board[8]:
        return True
    elif board[3] == board[6] and board[6] == board[9]:
        return True
    elif board[7] == board[5] and board[5] == board[3]:
        return True
    elif board[1] == board[5] and board[5] == board[9]:
        return True
    else:
        return False

def tic_tac_toe():
    player_1 = input("Player 1 (X): Please enter your name here:")
    player_2 = input("Player 2 (O): Please enter your name here:")

    board = {1: "1", 2: "2", 3: "3",
           4: "4", 5: "5", 6: "6",
           7: "7", 8: "8", 9: "9"}

    print_board(board)

    i = 1
    while i <= 9:
        try:
            token = 'X' if i % 2 != 0 else 'O'
            player = player_1 if i % 2 != 0 else player_2
            player_input = int(input(token + ": Enter your box number: "))

            if player_input < 1 or player_input > 9:
                raise Exception("Box number must be between 1 and 9. Try again.")
            if board[player_input] != str(player_input):
                raise Exception("This number is taken, try another number:")

            board[player_input] = token
            print_board(board)

            if determine_winner(board):
                print(player + " is the winner!")
                return
        except Exception as message:
            print(message.args[0])
            continue

        i += 1

    print("Boohoo! It's a draw!")

tic_tac_toe()












