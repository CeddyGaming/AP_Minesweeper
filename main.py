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

# Initialize pygame, and all of its inclusive modules
pygame.init()

# GAME CONSTANT VARIABLES
amount_of_rows = 18
screen_resolution = 360
bottom_rectangle_y = 20
size_of_square = screen_resolution / amount_of_rows
number_of_mines = 60
color_dictionary = {
    "square_accent_1": pygame.Color(107, 40, 40),  # Maroon
    "square_accent_2": pygame.Color(128, 128, 128),  # Gray
    "mine": pygame.Color(104, 182, 242),  # Light Blue
    "completed_square": pygame.Color(255, 255, 255),  # White
    "text_color": pygame.Color(0, 0, 0)  # Black
}

# INITIALIZE GAME
# This area of the program will initialize all of pygame's modules, set up a screen, and our bottom info rectangle.
screen = pygame.display.set_mode(size=(screen_resolution, screen_resolution + bottom_rectangle_y), flags=pygame.SCALED)
timer_event = USEREVENT
font = pygame.font.SysFont("comicsansms", 14)
font_big = pygame.font.SysFont("comicsansms", 42)
flag_image = pygame.image.load(os.path.join("flag.png")).convert_alpha()
red_x_image= pygame.image.load(os.path.join("red_x_large.png")).convert_alpha()
pygame.display.set_caption('Minesweeper')

information_rectangle = pygame.Rect((0, screen_resolution), (screen_resolution, bottom_rectangle_y))
pygame.draw.rect(screen, pygame.Color(255, 255, 255), information_rectangle)

timer_info_text = font.render("Timer: ", True, "Black")
timer_text = font.render("0", True, "Black")
flags_info_text = font.render("Flags Left: ", True, "Black")
flags_text = font.render(str(number_of_mines), True, "Black")

screen.blit(timer_info_text, (information_rectangle.left + 10, information_rectangle.top))
screen.blit(timer_text, (information_rectangle.left + timer_info_text.get_size()[0] + 10, information_rectangle.top))
screen.blit(flags_info_text, (information_rectangle.right - flags_text.get_size()[0] - flags_info_text.get_size()[0] - 10, information_rectangle.top))
screen.blit(flags_text, (information_rectangle.right - flags_text.get_size()[0] - 10, information_rectangle.top))

# GAME SESSION VARIABLES
is_game = False
is_endgame_displayed = True
timer = 0
flags_left = number_of_mines
squares = []

# GAME SQUARES SETUP
for row in range(amount_of_rows):
    RowOfSquares = []
    for col in range(amount_of_rows):
        info = {
            "rectangle":
                pygame.Rect(0 + col * size_of_square, 0 + row * size_of_square, size_of_square, size_of_square),
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

# FUNCTIONS
def reanimate_bottom_rectangle():
    global timer_info_text, timer_text, flags_info_text, flags_text, timer, flags_left
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), information_rectangle)
    timer_text = font.render(str(timer), True, "Black")
    flags_text = font.render(str(flags_left), True, "Black")
    screen.blit(timer_info_text, (information_rectangle.left + 10, information_rectangle.top))
    screen.blit(timer_text,(information_rectangle.left + timer_info_text.get_size()[0] + 10, information_rectangle.top))
    screen.blit(flags_info_text, (information_rectangle.right - flags_text.get_size()[0] - flags_info_text.get_size()[0] - 10, information_rectangle.top))
    screen.blit(flags_text, (information_rectangle.right - flags_text.get_size()[0] - 10, information_rectangle.top))


def get_square_from_pos(pos):
    global size_of_square, amount_of_rows, squares
    x = math.ceil(pos[0] / size_of_square) - 1
    y = math.ceil(pos[1] / size_of_square) - 1
    if (0 <= x) and (x <= amount_of_rows - 1):
        if (0 <= y) and (y <= amount_of_rows - 1):
            return squares[y][x]
    return False


def get_index_from_square(square):
    global squares
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
                if squares[cord[0]][cord[1]]["is_mine"]:
                    continue
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
                if squares[cord[0]][cord[1]]["is_cleared"]:
                    continue
                if squares[cord[0]][cord[1]] not in exempt_squares:
                    empty_square_list.append(squares[cord[0]][cord[1]])
                    squares[cord[0]][cord[1]]["is_cleared"] = True
                    squares[cord[0]][cord[1]]["color"] = "White"
    for square in empty_square_list:
        if square["mines_amount"] == 0:
            remove_empty_squares(get_index_from_square(square), empty_square_list)


def begin_game(square_pressed):
    global squares, flags_left, timer
    flags_left = number_of_mines
    timer = 0

    # Reset the colors of all the squares
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
    pygame.time.set_timer(timer_event, 1000)
    remove_empty_squares(get_index_from_square(square_pressed))


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

end_game_rectangle = pygame.Rect((screen_resolution / 4, screen_resolution / 4), (screen_resolution / 2, screen_resolution / 2 - 20))
def end_game(win):
    global is_game
    is_game = False
    pygame.time.set_timer(timer_event, 0)
    if not win:
        for row in squares:
            for col in row:
                if col["is_mine"] and not col["is_flagged"]:
                    pygame.draw.rect(screen, pygame.Color(0, 0, 255), col["rectangle"])
                    col["color"] = pygame.Color(0, 0, 255)
                if col["is_flagged"] and not col["is_mine"]:
                    wrong_mine_image = pygame.transform.scale(red_x_image, (size_of_square, size_of_square))
                    screen.blit(wrong_mine_image, (col["rectangle"].left, col["rectangle"].top))
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), end_game_rectangle)
        text = font_big.render("You lose!", True, "Black")
        text_rect = text.get_rect(center=end_game_rectangle.center)
        screen.blit(text, text_rect)
    else:
        text = font_big.render("You win!", True, "Black")
        text_rect = text.get_rect(center=end_game_rectangle.center)
        screen.blit(text, text_rect)


# GAME LOOP
while True:
    if is_game:
        for row in squares:
            for col in row:
                if col["is_cleared"]:
                    pygame.draw.rect(screen, pygame.Color(255, 255, 255), col["rectangle"])
                    col["color"] = pygame.Color(255, 255, 255)
                    text = font.render(str(col["mines_amount"]), True, "Black")
                    position_rectangle = text.get_rect()
                    position_rectangle.center = col["rectangle"].center
                    screen.blit(text, position_rectangle)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == USEREVENT:
            timer += 1
            reanimate_bottom_rectangle()
        elif event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            square = get_square_from_pos(mouse_pos)
            if not square:
                continue
            if is_game:
                if mouse[2]:
                    if not square["is_flagged"]:
                        transformedFlag = pygame.transform.scale(flag_image, (size_of_square, size_of_square))
                        screen.blit(transformedFlag, (square["rectangle"].left, square["rectangle"].top))
                        square["is_flagged"] = transformedFlag
                        flags_left -= 1
                    else:
                        pygame.draw.rect(screen, square["color"], square["rectangle"])
                        square["is_flagged"] = False
                        flags_left += 1
                elif square["is_mine"]:
                    end_game(False)
                elif square["mines_amount"] == 0:
                    remove_empty_squares(get_index_from_square(square))
                else:
                    square["is_cleared"] = True
            else:
                if is_endgame_displayed:
                    is_endgame_displayed = False
                    is_game = True
                    begin_game(square)
    pygame.display.update()

"""
Works Cited:
f
"""

# Flag image used in this program is public domain: CC0
