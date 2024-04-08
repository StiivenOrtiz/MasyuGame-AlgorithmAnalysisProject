# Imports
import pygame

import Util.colors as COLORS
import GUI.draw_game as draw_game
import Logic.mouse_controller as mc


class Game:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        # List to store the drawn lines
        self.drawn_lines = []

        # Define constants

        # Colors
        self.colors = COLORS.colors()

        # Screen size
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        # Frames per second
        self.FPS = 60

        # Screen margin
        self.MARGIN_SIZE = 64

        # Number of cells in a row or column
        self.N_CELLS = 10

        # Size of each cell
        self.CELL_SIZE = (self.SCREEN_WIDTH - 2 *
                          self.MARGIN_SIZE) // self.N_CELLS

        # Size of the button
        self.BUTTON_THEME_SIZE = 50
        self.BUTTON_THEME_X = self.SCREEN_WIDTH - self.BUTTON_THEME_SIZE - 10
        self.BUTTON_THEME_Y = 8

        # Button icon
        self.ICON_THEME_SIZE = 20
        self.ICON_THEME_X = self.BUTTON_THEME_X + \
            (self.BUTTON_THEME_SIZE - self.ICON_THEME_SIZE) // 2
        self.ICON_THEME_Y = self.BUTTON_THEME_Y + \
            (self.BUTTON_THEME_SIZE - self.ICON_THEME_SIZE) // 2

        self.circle_data = {
            (1, 3): 1,
            (1, 5): 1,
            (2, 5): 1,
            (2, 9): 2,
            (3, 3): 2,
            (3, 5): 2,
            (3, 7): 1,
            (4, 4): 1,
            (4, 7): 1,
            (5, 1): 2,
            (5, 6): 1,
            (5, 10): 1,
            (6, 3): 1,
            (6, 8): 1,
            (7, 3): 2,
            (7, 7): 1,
            (8, 1): 1,
            (8, 5): 2,
            (8, 10): 1,
            (9, 7): 1,
            (9, 8): 1,
            (10, 3): 2,
            (10, 10): 2,
        }

        self.prev_cell_clicked = (-10, -10)

    def draw(self, screen, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the theme button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.BUTTON_THEME_X <= mouse_x <= self.BUTTON_THEME_X + self.BUTTON_THEME_SIZE and \
                        self.BUTTON_THEME_Y <= mouse_y <= self.BUTTON_THEME_Y + self.BUTTON_THEME_SIZE:
                    self.colors.change_dark_mode()

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.drawn_lines, self.prev_cell_clicked = mc.detects_lines(
            mouse_buttons, mouse_pos, self.CELL_SIZE, self.MARGIN_SIZE, self.N_CELLS, self.prev_cell_clicked, self.drawn_lines)

        screen.fill(self.colors.BLACK)

        draw_game.drawAll(
            screen,
            self.N_CELLS,
            self.CELL_SIZE,
            self.MARGIN_SIZE,
            self.BUTTON_THEME_SIZE,
            self.BUTTON_THEME_X,
            self.BUTTON_THEME_Y,
            self.ICON_THEME_SIZE,
            self.ICON_THEME_X,
            self.ICON_THEME_Y,
            self.circle_data,
            self.drawn_lines,
            self.colors)
