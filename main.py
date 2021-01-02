import random
import numpy as np
import pygame
import sys

import math
from functions import create_board, print_board, draw_board, is_valid_location, get_free_row, place_piece, \
    winning_move, minmax
from init import COLUMN_COUNT, ROW_COUNT, opponent, turn

PLAYER = 1
AI = 3
PLAYER2 = 2

EMPTY = 0
PLAYER_PIECE = 1
PLAYER2_PIECE = 2
AI_PIECE = 2

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SQUARESIZE = 75
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
RADIUS = int(SQUARESIZE / 2 - 5)

board = create_board()
print_board(board)
game_over = False

# initiating the game
pygame.init()
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("monospace", int(height / 10))

# in case the opponent is human
if opponent == PLAYER2:

    # we draw the board immediately
    draw_board(board)
    pygame.display.update()

    while not game_over:

        # handling the event of "closing the game through the exit button"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # used for the scroll bar above the game board
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                px = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (px, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (px, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            # used for handling clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))

                # Human 1
                if turn == PLAYER:
                    px = event.pos[0]
                    col = int(math.floor(px / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_free_row(board, col)
                        place_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = font.render("Player 1 wins!", 1, BLACK)
                            screen.blit(label, (40, 10))
                            game_over = True

                        if opponent == PLAYER2:
                            turn = PLAYER2
                        elif opponent == AI:
                            turn = AI

                        print_board(board)
                        draw_board(board)

                # Human 2
                elif turn == PLAYER2:
                    px = event.pos[0]
                    col = int(math.floor(px / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_free_row(board, col)
                        place_piece(board, row, col, PLAYER2_PIECE)

                        if winning_move(board, PLAYER2_PIECE):
                            label = font.render("Player 2 wins!", 1, BLACK)
                            screen.blit(label, (40, 10))
                            game_over = True
                        turn = PLAYER

                        print_board(board)
                        draw_board(board)
        if game_over:
            pygame.time.wait(3000)

# in case opponent is the computer
if opponent == AI:

    # we make an intermediate screen where player chooses AI level
    pygame.draw.rect(screen, WHITE, (0, 0, width, height))
    pygame.draw.rect(screen, RED, (0, 2 * width / 3, width, height / 3))
    pygame.draw.rect(screen, YELLOW, (0, width / 3, width, height / 3))
    pygame.draw.rect(screen, WHITE, (0, 0, width, height / 3))
    label = font.render("EASY", 10, BLACK)
    screen.blit(label, (height / 3, width / 9))
    label = font.render("NORMAL", 10, BLACK)
    screen.blit(label, (height / 4, 4 * width / 9))
    label = font.render("HARD", 10, BLACK)
    screen.blit(label, (height / 3, 7 * width / 9))
    pygame.display.update()
    ok = 0
    choice = 0
    while not ok:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # player has to click in order to choose AI level
            if event.type == pygame.MOUSEBUTTONDOWN:
                py = event.pos[1]
                print(py)
                print(height)
                if py < height / 3:
                    choice = 0
                    ok = 1
                if py > height / 3 and py < 2 * height / 3:
                    choice = 1
                    ok = 1
                if py > 2 * height / 3 and py < height:
                    choice = 2
                    ok = 1

    # after he chooses the difficulty, the game board appears
    draw_board(board)
    pygame.display.update()

    while not game_over:

        # handling the event of "closing the game through the exit button"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # used for the scroll bar above the game board
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))
                px = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (px, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (px, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            # used for handling clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARESIZE))

                # human turn
                if turn == PLAYER:
                    px = event.pos[0]
                    col = int(math.floor(px / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_free_row(board, col)
                        place_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = font.render("Player 1 wins!", 1, BLACK)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn = AI

                        print_board(board)
                        draw_board(board)

        # AI turn
        if turn == AI and not game_over:
            # Hard difficulty
            if choice == 2:
                col, minmax_score = minmax(board, 5, -math.inf, math.inf, True)
            # Medium difficulty
            if choice == 1:
                col, minmax_score = minmax(board, 1, -math.inf, math.inf, True)
            # Easy difficulty
            if choice == 0:
                col = random.randint(0, COLUMN_COUNT - 1)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_free_row(board, col)
                place_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = font.render("AI wins!", 1, BLACK)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = PLAYER

                print_board(board)
                draw_board(board)

        if game_over:
            pygame.time.wait(3000)
