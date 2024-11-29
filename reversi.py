import copy
from time import sleep as delay

# ========== Variables ==========

# Color codes for the game
RESET_COLOR = '\033[0m'
RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
YELLOW_COLOR = '\033[93m'
BLUE_COLOR = '\033[94m'
WHITE_COLOR = '\033[97m'
BLACK_COLOR = '\033[30m'
BLACK_CIRCLE = "\u25CF"  
WHITE_CIRCLE = "\u25CB" 
# Global variables for the game
SEARCH_DEPTH = 4
PLAYER_X = "X" # White
PLAYER_O = "O" # Black
BOARD_SIZE = 8
EMPTY_CELL = "."
BOARD = [[EMPTY_CELL for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
BOARD[BOARD_SIZE//2-1][BOARD_SIZE//2-1] , BOARD[BOARD_SIZE//2-1][BOARD_SIZE//2] = PLAYER_X , PLAYER_O
BOARD[BOARD_SIZE//2][BOARD_SIZE//2-1] , BOARD[BOARD_SIZE//2][BOARD_SIZE//2] = PLAYER_O , PLAYER_X

# ========== Game Board implementation ==========

# Print the board with circles
def print_board(board):
    print("  ", end="")
    for i in range(BOARD_SIZE):
        print(f"  {BLUE_COLOR}{chr(i + 65)}{RESET_COLOR} ", end="")
    print()
    print("  ", end="")
    print("+" + "---+" * BOARD_SIZE)

    for i in range(BOARD_SIZE):
        print(f"{BLUE_COLOR}{i + 1}{RESET_COLOR} |", end="")
        for j in range(BOARD_SIZE):
            if board[i][j] == PLAYER_X:
                print(f" {WHITE_COLOR}●{RESET_COLOR} |", end="")
            elif board[i][j] == PLAYER_O:
                print(f" {BLACK_COLOR}●{RESET_COLOR} |", end="")
            elif board[i][j] == f"{RED_COLOR}*{RESET_COLOR}":
                print(f" {RED_COLOR}*{RESET_COLOR} |", end="")
            else:
                print("   |", end="")
        print()
        print("  ", end="")
        print("+" + "---+" * BOARD_SIZE)

# Checking whether if a move is valid or not 
def is_valid_move(board , row , col , player) :
    if board[row][col] != EMPTY_CELL and not is_game_over(board) :
        return False

    OPPONENT = PLAYER_O if player == PLAYER_X else PLAYER_X

    for row_direction , col_direction in [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]:
        r = row + row_direction 
        c = col + col_direction 
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == OPPONENT and board[r][c] != EMPTY_CELL:
            r += row_direction
            c += col_direction 
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player :
                return True
    return False

# Finding all valid moves based on is_valid_move function
def all_valid_moves(board , player) :
    valid_moves = []

    for i in range(BOARD_SIZE) :
        for j in range(BOARD_SIZE) :
            if is_valid_move(board , i , j , player) :
                valid_moves.append((i , j))
    return valid_moves

# Movements based on validation , flip opponent's bead if it's in a line  
def make_move(board , row , col , player) :
    if not is_valid_move(board , row , col , player) :
        return False
    
    OPPONENT = PLAYER_O if player == PLAYER_X else PLAYER_X
    board[row][col] = player

    for row_direction , col_direction in [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]:
        r = row + row_direction
        c = col + col_direction 
        flip = []
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == OPPONENT and board[r][c] != EMPTY_CELL:
            flip.append((r , c))
            r += row_direction
            c += col_direction
            if 0 <= r < BOARD_SIZE and 0<= c < BOARD_SIZE and board[r][c] == player :
                for flip_row , flip_col in flip :
                    board[flip_row][flip_col] = player
    return True 

# Print all available moves using (all_valid_moves)
def all_available_moves(board , player) :
    valid_moves = all_valid_moves(board , player)
    new_board = copy.deepcopy(board)
    for move_r, move_c in valid_moves :
        new_board[move_r][move_c] = f"{RED_COLOR}*{RESET_COLOR}"
    print_board(new_board)

# Calculate the player X and player O
def count_score(board):
    x_count = 0
    o_count = 0
    for row in board:
        x_count += row.count(PLAYER_X)
        o_count += row.count(PLAYER_O)
    return x_count, o_count

# The game is if there are no move left
def is_game_over(board) :
    return sum(row.count(EMPTY_CELL) for row in board) == 0

# ========== Ai and Player Implementation ==========

# Implement AI movements based on minimax algorithm
def minimax(board , maximizing_player , depth , alpha , beta , player) :
    if depth == 0 or is_game_over(board) :
        return count_score(board)[0] if player == PLAYER_X else count_score(board)[1], None, None
    
    OPPONENT = PLAYER_O if player == PLAYER_X else PLAYER_X
    
    if all_valid_moves(board , player) :
        valid_moves = all_valid_moves(board , player)
    else : 
        return 0 , 0 , 0 

    if maximizing_player :
        best_row, best_col = None, None
        max_eval = float("-inf")

        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board , move[0] , move[1] , player)
            eval , _ , _ = minimax(new_board , False , depth - 1 , alpha , beta , OPPONENT) 
            if eval > max_eval:
                max_eval = eval
                best_row, best_col = move
            alpha = max(alpha , eval) 
            if beta <= alpha :
                break
        return max_eval, best_row, best_col
    else : 
        min_eval = float("inf")
        best_row, best_col = None, None

        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board , move[0] , move[1] , player)
            eval , _ , _ = minimax(new_board , True , depth - 1 , alpha , beta , OPPONENT)
            
            if eval < min_eval:
                min_eval = eval
                best_row, best_col = move
            beta = min(beta , eval)
            if beta >= alpha : 
                break
        return min_eval, best_row, best_col

# Implementation of the way that human player can make movements and play
def player(board, current_player):
    while True:
        try:
            all_available_moves(board, current_player)
            position = input(f"\nPlayer {current_player}, please enter your move (ex: C5): ").strip().upper()

            if len(position) != 2 or not position[0].isalpha() or not position[1].isdigit():
                print("Invalid input format! Please enter in the format 'LetterNumber', ex: C5.")
                continue

            col = position[0]
            if col < 'A' or col > 'H':
                print("Invalid column! Please enter a column letter from A to H.")
                continue

            row = int(position[1]) - 1
            col = ord(col) - 65

            if is_valid_move(board, row, col, current_player):
                make_move(board, row, col, current_player)
                print(f"\nPlayer {current_player} plays: {chr(65 + col)}{row + 1}\n")
                break
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Invalid input! Please enter valid row and column.")
            
# ========== Game option implementation ==========

# Player vs Player option
def player_vs_player():
    board = copy.deepcopy(BOARD)
    current_player = PLAYER_X

    while not is_game_over(board):
        player(board , current_player)
        current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O

    print_board(board)
    x_score, o_score = count_score(board)
    print(f"X Score: {x_score}, O Score: {o_score}")

    if x_score > o_score:
        print("X wins!")
    elif o_score > x_score:
        print("O wins!")
    else:
        print("It's a tie!")

# Player vs AI option
def player_vs_ai():
    board = copy.deepcopy(BOARD)
    current_player = PLAYER_X
    depth = SEARCH_DEPTH  

    while not is_game_over(board):
        if current_player == PLAYER_X:
            player(board , current_player)
        else: 
            _, best_row, best_col = minimax(board, True , depth , float('-inf'), float('inf'), current_player)
            make_move(board, best_row, best_col, current_player)
            print(f"Computer plays: {chr(65 + best_col)}{best_row + 1}")

        current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O
    
    x_score , o_score = count_score(board)
    print_board(board)
    print(f"X Score: {x_score}, O Score: {o_score}")
    
    if x_score > o_score:
        print("X wins!")
    elif o_score > x_score:
        print("O wins!")
    else:
        print("It's a tie!")

# Computer vs Computer option
def computer_vs_computer() :
    board = copy.deepcopy(BOARD)
    current_player= PLAYER_X
    depth = SEARCH_DEPTH 
    
    while not is_game_over(board) :
        if current_player == PLAYER_X :
            _ , best_row , best_col = minimax(board , True , depth , float("-inf") , float("+inf") , current_player)
            make_move(board , best_row , best_col , current_player)
        else : 
            _ , best_row , best_col = minimax(board , False , depth , float("-inf") , float("+inf") , current_player)
            make_move(board , best_row , best_col , current_player)
        
        current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O 
    
        delay(0.3)
        print_board(board)
        print(f"Computer {current_player} plays: {chr(65 + best_col)}{best_row + 1}")
        
    x_score , o_score = count_score(board)
    print(f"X score : {x_score} , O score {o_score}")
    
    if x_score > o_score:
        print("X wins!")
    elif o_score > x_score:
        print("O wins!")
    else:
        print("It's a tie!")

# ========== Main implementation ==========

# Print out the option for the game, handle the invalid input and exceptions
if __name__ == "__main__":
    play_again = True
    while play_again:
        try:
            print("Welcome to Reversi Game!")
            print("Secure more beads than your opponent to win the game.")
            print("X is White and O is Black.")
            print("Select your choice to play the game:")
            option = int(input("1. Player vs Player\n2. Player vs AI\n3. Computer vs Computer\nEnter your choice (1/2/3): "))
            if option == 1:
                player_vs_player()
            elif option == 2:
                player_vs_ai()
            elif option == 3:
                computer_vs_computer()
            else:
                print("Invalid option! Please try again.")
        except KeyboardInterrupt:
            break
        except TypeError:
            print("No more moves are available!")
        finally:
            print("Game over!")