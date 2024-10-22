import pygame
import sys
import numpy as np

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

# Function to create the game board
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

# Main loop to handle game events and rendering
def main():
    board = create_board()
    game_over = False
    turn = 0

    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                draw_board(board)

                # Switch to the next player
                turn += 1
                turn = turn % 2

if __name__ == "__main__":
    main()