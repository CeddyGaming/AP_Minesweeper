"""
Minesweeper Recreation
AP Computer Science Principals

Cedric Tabban
"""
# Import modules for minesweeper
import pygame
import math
import os
import random
import sys
from pygame.locals import *

# GAME CONSTANT VARIABLES
amount_of_rows = 18
screen_resolution = 360
size_of_square = screen_resolution / amount_of_rows
number_of_mines = 60

# INITIALIZE GAME
pygame.init()
screen = pygame.display.set_mode(size=(screen_resolution, screen_resolution), flags=pygame.SCALED)
font = pygame.font.SysFont("comicsansms", 12)
fontBig = pygame.font.SysFont("comicsansms", 42)
flagImage = pygame.image.load(os.path.join("flag.png")).convert_alpha()
pygame.display.set_caption('Minesweeper')

# GAME SESSION VARIABLES
is_game = False
flags_left = number_of_mines


# FUNCTIONS

def get_square_from_pos(pos):
    x = math.ceil(pos[0] / size_of_square) - 1
    y = math.ceil(pos[1] / size_of_square) - 1
    print((x, y))
    return squares[y][x]


def get_index_from_square(square):
    row_number = 0
    for row in squares:
        col_number = 0
        for col in row:
            if (col["rectangle"].top == square["rectangle"].top) and (
                    col["rectangle"].left == square["rectangle"].left):
                return (row_number, col_number)
            col_number += 1
        row_number += 1


def set_around_mines(pos):
    neighbor_cords = [(pos[0] - 1, pos[1] - 1), (pos[0], pos[1] - 1),
                      (pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1]),
                      (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1] + 1),
                      (pos[0], pos[1] + 1), (pos[0] + 1, pos[1] + 1)]
    for cord in neighbor_cords:
        if (0 <= cord[0]) and (cord[0] <= amount_of_rows - 1):
            if (0 <= cord[1]) and (cord[1] <= amount_of_rows - 1):
                squares[cord[0]][cord[1]]["mines_amount"] = squares[cord[0]][cord[1]]["mines_amount"] + 1


def remove_empty_squares(pos, exempt_squares=()):
    neighbor_cords = [(pos[0] - 1, pos[1] - 1), (pos[0], pos[1] - 1),
                      (pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1]),
                      (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1] + 1),
                      (pos[0], pos[1] + 1), (pos[0] + 1, pos[1] + 1)]
    squares[pos[0]][pos[1]]["is_cleared"] = True
    empty_square_list = []
    for cord in neighbor_cords:
        if (0 <= cord[0]) and (cord[0] <= amount_of_rows - 1):
            if (0 <= cord[1]) and (cord[1] <= amount_of_rows - 1):
                if squares[cord[0]][cord[1]] not in exempt_squares:
                    empty_square_list.append(squares[cord[0]][cord[1]])
                    squares[cord[0]][cord[1]]["is_cleared"] = True
                    squares[cord[0]][cord[1]]["color"] = "White"
    print(empty_square_list)
    for square in empty_square_list:
        if square["mines_amount"] == 0:
            remove_empty_squares(get_index_from_square(square), empty_square_list)


def begin_game(square_pressed):
    # Mass list for sampling, exception on square that was clicked
    mass_square_list = []
    for row in squares:
        for col in row:
            if col == square_pressed:
                continue
            mass_square_list.append(col["rectangle"])
    # Randomize mines, count mines around each square.
    random_mine_list = random.sample(mass_square_list, number_of_mines)
    row_number = 0
    for row in squares:
        col_number = 0
        for col in row:
            for mine in random_mine_list:
                if (col["rectangle"].top == mine.top) and (col["rectangle"].left == mine.left):
                    col["is_mine"] = True
                    set_around_mines((row_number, col_number))
            col_number += 1
        row_number += 1
    remove_empty_squares(get_index_from_square(square_pressed))


squares = []

for row in range(amount_of_rows):
    RowOfSquares = []
    for col in range(amount_of_rows):
        info = {
            "rectangle":
                pygame.Rect(0 + col * size_of_square, 0 + row * size_of_square,
                            size_of_square, size_of_square),
            "is_mine":
                False,
            "mines_amount":
                0,
            "is_flagged":
                False,
            "is_cleared":
                False,
            "color":
                False
        }
        RowOfSquares.append(info)
    squares.append(RowOfSquares)

rowindex = 0
for row in squares:
    for col in range(len(row)):
        if rowindex % 2:
            if col % 2:
                pygame.draw.rect(screen, "Red", row[col]["rectangle"])
                row[col]["color"] = "Red"
            else:
                pygame.draw.rect(screen, "Gray", row[col]["rectangle"])
                row[col]["color"] = "Gray"
        else:
            if col % 2:
                pygame.draw.rect(screen, "Gray", row[col]["rectangle"])
                row[col]["color"] = "Gray"
            else:
                pygame.draw.rect(screen, "Red", row[col]["rectangle"])
                row[col]["color"] = "Red"
    rowindex += 1


def end_game(win):
    information_rectangle = pygame.Rect(screen_resolution / 4,
                                        screen_resolution / 4,
                                        screen_resolution / 2,
                                        screen_resolution / 2 - 20)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), information_rectangle)
    text = fontBig.render("You win!", True, "Black")
    text_rect = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, text_rect)


# GAME LOOP
while True:
    if is_game:
        for row in squares:
            for col in row:
                if col["is_mine"]:
                    pygame.draw.rect(screen, pygame.Color(0, 0, 255), col["rectangle"])
                    col["color"] = pygame.Color(0, 0, 255)
                else:
                    text = font.render(str(col["mines_amount"]), True, "Black")
                    position_rectangle = text.get_rect()
                    position_rectangle.center = col["rectangle"].center
                    screen.blit(text, position_rectangle)
                if col["is_cleared"]:
                    pygame.draw.rect(screen, "White", col["rectangle"])

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            square = get_square_from_pos(mouse_pos)
            if is_game:
                if mouse[2]:
                    if not square["is_flagged"]:
                        transformedFlag = pygame.transform.scale(
                            flagImage, (size_of_square, size_of_square))
                        screen.blit(transformedFlag,
                                    (square["rectangle"].left, square["rectangle"].top))
                        square["is_flagged"] = transformedFlag
                    else:
                        pygame.draw.rect(screen, square["color"], square["rectangle"])
                        square["is_flagged"] = False
                elif square["is_mine"]:
                    end_game(False)
            else:
                begin_game(square)
                is_game = True
    pygame.display.update()

"""
Works Cited:
f
"""

# Flag image used in this program is public domain: CC0
