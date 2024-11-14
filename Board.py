import pygame
import sys
import numpy as np
import math

# Initialize pygame
pygame.init()

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the display
screen = pygame.display.set_mode(size)

# Create the game board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Function to drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if a column is valid for a move
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Function to get the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to draw the Connect 4 board on the screen
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int((r + 1) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Display the winner of the game
def display_winner(winner_name):
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(f"{winner_name} Wins!", True, WHITE)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(5000)  # Pause for 5 seconds
    pygame.quit()

# Checks for the winning move
def winning_move(board, piece):
    # Horizontal check
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Diagonal check /
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Diagonal check \
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Evaluation function for the AI
def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    # Center Column Score
    center_array = [int(board[r][COLUMN_COUNT // 2]) for r in range(ROW_COUNT)]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal, vertical, and diagonal scoring
    for r in range(ROW_COUNT):
        row_array = [int(board[r][c]) for c in range(COLUMN_COUNT)]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)
    for c in range(COLUMN_COUNT):
        col_array = [int(board[r][c]) for r in range(ROW_COUNT)]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
    return score

# Minimax with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 2))

    if maximizingPlayer:
        value = -math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# Main game loop
def main():
    game_mode = int(sys.argv[1])
    ai_difficulty = int(sys.argv[2]) if game_mode == 1 else None
    AI_DEPTH = {1: 1, 3: 2, 5: 4}.get(ai_difficulty, 1) if ai_difficulty else None

    board = create_board()
    game_over = False
    turn = 0
    moves = 0
    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if game_mode == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1 if turn == 0 else 2)
                    if winning_move(board, 1 if turn == 0 else 2):
                        draw_board(board)
                        game_over = True
                        winner = "Red" if turn == 0 else "Yellow"
                        display_winner(winner)

                    draw_board(board)
                    turn = (turn + 1) % 2
                    moves += 1

            if game_mode == 1 and event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        draw_board(board)
                        game_over = True
                        display_winner("Player")

                    draw_board(board)
                    turn += 1

            if game_mode == 1 and turn == 1 and not game_over:
                col, _ = minimax(board, AI_DEPTH, -math.inf, math.inf, True)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board, 2):
                        draw_board(board)
                        game_over = True
                        display_winner("AI")
                    
                    draw_board(board)
                    turn = (turn + 1) % 2

        if moves == 42:
            font = pygame.font.SysFont("Arial", 50)
            text = font.render("Game Tied", True, WHITE)
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(5000)  # Pause for 5 seconds
            game_over = True
            pygame.quit()

        
        if game_over:
            pygame.time.wait(5000)

if __name__ == "__main__":
    main()
