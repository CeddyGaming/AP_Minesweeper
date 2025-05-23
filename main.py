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
    "square_accent_1": pygame.Color(75, 5, 5),  # Dark Red
    "square_accent_2": pygame.Color(90, 10, 5),  # Bright Red
    "mine": pygame.Color(255, 0, 0),  # Light Blue
    "completed_square": pygame.Color(255, 255, 255),  # White
    "text_color": pygame.Color(0, 0, 0),  # Black
    "information_color": pygame.Color(255, 255, 255)  # White
}

# INITIALIZE GAME
# This area of the program will set up a screen, and our bottom info rectangle.
screen = pygame.display.set_mode(size=(screen_resolution, screen_resolution + bottom_rectangle_y), flags=pygame.SCALED)
timer_event = USEREVENT
font = pygame.font.SysFont("comicsansms", 14)
font_big = pygame.font.SysFont("comicsansms", 42)
flag_image = pygame.image.load(os.path.join("flag.png")).convert_alpha()
red_x_image = pygame.image.load(os.path.join("red_x_large.png")).convert_alpha()
pygame.display.set_caption('Minesweeper')

information_rectangle = pygame.Rect((0, screen_resolution), (screen_resolution, bottom_rectangle_y))
pygame.draw.rect(screen, color_dictionary["information_color"], information_rectangle)

timer_info_text = font.render("Timer: ", True, color_dictionary["text_color"])
timer_text = font.render("0", True, color_dictionary["text_color"])
flags_info_text = font.render("Flags Left: ", True, color_dictionary["text_color"])
flags_text = font.render(str(number_of_mines), True, color_dictionary["text_color"])

# GAME SESSION VARIABLES
is_game = False
is_endgame_displayed = True
timer = 0
flags_left = number_of_mines
squares = []


# FUNCTIONS
def reanimate_bottom_rectangle():
    global timer_info_text, timer_text, flags_info_text, flags_text, timer, flags_left
    pygame.draw.rect(screen, color_dictionary["information_color"], information_rectangle)
    timer_text = font.render(str(timer), True, color_dictionary["text_color"])
    flags_text = font.render(str(flags_left), True, color_dictionary["text_color"])
    screen.blit(timer_info_text, (information_rectangle.left + 10, information_rectangle.top + (
                information_rectangle.height - timer_info_text.get_size()[1]) / 2))
    screen.blit(timer_text, (information_rectangle.left + timer_info_text.get_size()[0] + 10,
                             information_rectangle.top + (information_rectangle.height - timer_text.get_size()[1]) / 2))
    screen.blit(flags_info_text, (
    information_rectangle.right - flags_text.get_size()[0] - flags_info_text.get_size()[0] - 10,
    information_rectangle.top + (information_rectangle.height - timer_text.get_size()[1]) / 2))
    screen.blit(flags_text, (information_rectangle.right - flags_text.get_size()[0] - 10,
                             information_rectangle.top + (information_rectangle.height - timer_text.get_size()[1]) / 2))


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


def get_neighbor_squares(pos):
    neighbor_cords = [(pos[0] - 1, pos[1] - 1), (pos[0], pos[1] - 1),
                      (pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1]),
                      (pos[0] + 1, pos[1]), (pos[0] - 1, pos[1] + 1),
                      (pos[0], pos[1] + 1), (pos[0] + 1, pos[1] + 1)]
    verified_square_positions = []
    for cord in neighbor_cords:
        if (0 <= cord[0]) and (cord[0] <= amount_of_rows - 1):
            if (0 <= cord[1]) and (cord[1] <= amount_of_rows - 1):
                verified_square_positions.append(cord)
    return verified_square_positions


def set_around_mines(pos):
    neighbor_cords = get_neighbor_squares(pos)
    for cord in neighbor_cords:
        if squares[cord[0]][cord[1]]["is_mine"]:
            continue
        squares[cord[0]][cord[1]]["mines_amount"] = squares[cord[0]][cord[1]]["mines_amount"] + 1


def remove_empty_squares(pos, exempt_squares=()):
    neighbor_cords = get_neighbor_squares(pos)
    squares[pos[0]][pos[1]]["is_cleared"] = True
    empty_square_list = []
    for cord in neighbor_cords:
        if squares[cord[0]][cord[1]]["is_cleared"]:
            continue
        if squares[cord[0]][cord[1]] not in exempt_squares:
            empty_square_list.append(squares[cord[0]][cord[1]])
            squares[cord[0]][cord[1]]["is_cleared"] = True
    for square in empty_square_list:
        if square["mines_amount"] == 0:
            remove_empty_squares(get_index_from_square(square), empty_square_list)


def begin_game(square_pressed):
    # Mass list for sampling, exception on square that was clicked
    exempt_squares = [square_pressed]
    mass_square_list = []
    neighbor_of_pressed = get_neighbor_squares(get_index_from_square(square_pressed))
    for cord in neighbor_of_pressed:
        exempt_squares.append(squares[cord[0]][cord[1]])
    for row in squares:
        for col in row:
            if col in exempt_squares:
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


end_game_rectangle = pygame.Rect((screen_resolution / 4, screen_resolution / 4),
                                 (screen_resolution / 2, screen_resolution / 2 - 20))
transparent_surface = pygame.Surface(end_game_rectangle.size, pygame.SRCALPHA)


def end_game(win):
    global is_game, is_endgame_displayed
    is_game = False
    is_endgame_displayed = True
    pygame.time.set_timer(timer_event, 0)
    if not win:
        for row in squares:
            for col in row:
                if col["is_mine"] and not col["is_flagged"]:
                    pygame.draw.rect(screen, color_dictionary["mine"], col["rectangle"])
                    col["color"] = color_dictionary["mine"]
                if col["is_flagged"] and not col["is_mine"]:
                    wrong_mine_image = pygame.transform.scale(red_x_image, (size_of_square, size_of_square))
                    screen.blit(wrong_mine_image, (col["rectangle"].left, col["rectangle"].top))

        text = font_big.render("You lose!", True, color_dictionary["text_color"])
        text_rect = text.get_rect(center=end_game_rectangle.center)
        pygame.draw.rect(transparent_surface, pygame.Color(255, 255, 255, 210), transparent_surface.get_rect())
        screen.blit(transparent_surface, end_game_rectangle)
        screen.blit(text, text_rect)
    else:
        text = font_big.render("You win!", True, color_dictionary["text_color"])
        text_rect = text.get_rect(center=end_game_rectangle.center)
        pygame.draw.rect(transparent_surface, pygame.Color(255, 255, 255, 210), transparent_surface.get_rect())
        screen.blit(transparent_surface, end_game_rectangle)
        screen.blit(text, text_rect)


def reset_game():
    global squares, flags_left, timer
    flags_left = number_of_mines
    squares = []
    timer = 0
    # Reset squares
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
    rowindex = 0
    for row in squares:
        for col in range(len(row)):
            if rowindex % 2:
                if col % 2:
                    pygame.draw.rect(screen, color_dictionary["square_accent_1"], row[col]["rectangle"])
                    row[col]["color"] = color_dictionary["square_accent_1"]
                else:
                    pygame.draw.rect(screen, color_dictionary["square_accent_2"], row[col]["rectangle"])
                    row[col]["color"] = color_dictionary["square_accent_2"]
            else:
                if col % 2:
                    pygame.draw.rect(screen, color_dictionary["square_accent_2"], row[col]["rectangle"])
                    row[col]["color"] = color_dictionary["square_accent_2"]
                else:
                    pygame.draw.rect(screen, color_dictionary["square_accent_1"], row[col]["rectangle"])
                    row[col]["color"] = color_dictionary["square_accent_1"]
        rowindex += 1
    reanimate_bottom_rectangle()


reset_game()
text = font.render("Begin by clicking a square.", True, color_dictionary["text_color"])
text_rect = text.get_rect(center=end_game_rectangle.center)
pygame.draw.rect(transparent_surface, pygame.Color(255, 255, 255, 210), transparent_surface.get_rect())
screen.blit(transparent_surface, end_game_rectangle)
screen.blit(text, text_rect)

# GAME LOOP
while True:
    is_game_won = True
    if is_game:
        for row in squares:
            for col in row:
                if col["is_cleared"]:
                    pygame.draw.rect(screen, color_dictionary["completed_square"], col["rectangle"])
                    col["color"] = color_dictionary["completed_square"]
                    if col["mines_amount"] != 0:
                        text = font.render(str(col["mines_amount"]), True, color_dictionary["text_color"])
                        position_rectangle = text.get_rect()
                        position_rectangle.center = col["rectangle"].center
                        screen.blit(text, position_rectangle)
                elif not col["is_cleared"] and not col["is_mine"]:
                    is_game_won = False
        if is_game_won:
            end_game(True)
            continue
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
                        square["is_flagged"] = True
                        flags_left -= 1
                    else:
                        pygame.draw.rect(screen, square["color"], square["rectangle"])
                        square["is_flagged"] = False
                        flags_left += 1
                    reanimate_bottom_rectangle()
                elif square["is_mine"] and not square["is_flagged"]:
                    end_game(False)
                elif (square["mines_amount"] == 0) and not square["is_flagged"]:
                    remove_empty_squares(get_index_from_square(square))
                elif not square["is_flagged"]:
                    square["is_cleared"] = True
            else:
                if not is_endgame_displayed:
                    is_game = True
                    begin_game(square)
                else:
                    is_endgame_displayed = False
                    reset_game()
    pygame.display.update()

"""
Works Cited:
f
"""

# Flag image used in this program is public domain: CC0
