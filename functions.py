import random

import numpy as np
import pygame
import sys
import math

from init import ROW_COUNT, COLUMN_COUNT

PLAYER = 0
AI = 1
PLAYER2 = 1

EMPTY = 0
PLAYER_PIECE = 1
PLAYER2_PIECE = 2
AI_PIECE = 2

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


# initializes the board by filling it with zeros
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# checks if you can place a piece there
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


# place a piece in a specified location
def place_piece(board, row, col, piece):
    board[row][col] = piece


# returns the first available row
def get_free_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# checks if, after a move, a player has won
def winning_move(board, piece):
    # horizontally
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # vertically
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # diagonal "/////"
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # diagonal "\\\\\"
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


SQUARESIZE = 75
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
RADIUS = int(SQUARESIZE / 2 - 5)


# function to evaluate how many points each row gives
def eval(connected_line, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if connected_line.count(piece) == 4:
        score += 100
    elif connected_line.count(piece) == 3 and connected_line.count(EMPTY) == 1:
        score += 5
    elif connected_line.count(piece) == 2 and connected_line.count(EMPTY) == 2:
        score += 2

    if connected_line.count(opp_piece) == 3 and connected_line.count(EMPTY) == 1:
        score -= 4

    return score


# function to calculate score
def calculate_score(board, piece):
    score = 0

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            connected_line = row_array[c:c + 4]
            score += eval(connected_line, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            connected_line = col_array[r:r + 4]
            score += eval(connected_line, piece)

    # Score diagonal "/////"
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            connected_line = [board[r + i][c + i] for i in range(4)]
            score += eval(connected_line, piece)

    # Score diagonal "\\\\\"
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            connected_line = [board[r + 3 - i][c + i] for i in range(4)]
            score += eval(connected_line, piece)

    return score


# checks if a board is in the final state
def is_final_state(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# the minmax algorithm with alpha-beta prunning
def minmax(board, level, alpha, beta, is_maximizing_level):
    valid_locations = get_valid_locations(board)
    is_final = is_final_state(board)
    if level == 0 or is_final:
        if is_final:
            if winning_move(board, AI_PIECE):
                return None, 100000000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000000000
            else:  # game is over, no more valid moves
                return None, 0
        else:  # level is zero
            return None, calculate_score(board, AI_PIECE)

    if is_maximizing_level:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_free_row(board, col)
            b_copy = board.copy()
            place_piece(b_copy, row, col, AI_PIECE)
            new_score = minmax(b_copy, level - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:  # Minimizing level
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_free_row(board, col)
            b_copy = board.copy()
            place_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minmax(b_copy, level - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


# returns all valid locations
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# draws the board
def draw_board(board):
    # for empty spaces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLACK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, WHITE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # for actual pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == PLAYER2_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


# printing the board(in console)
def print_board(board):
    print(np.flip(board, 0))
