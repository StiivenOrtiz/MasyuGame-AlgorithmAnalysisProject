import pygame

import Util.colors as COLORS
import GUI.draw_game as draw_game
from Controllers.mouse_controller import MouseController
from Logic.game import Game_flow


class Game:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, filename):
        # List to store the drawn lines
        self.drawn_lines = []
        self.filename = filename
        
        # Create the graph
        self.game = Game_flow(self.filename)
        self.mc = MouseController(self.game)

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
        self.N_CELLS = self.game.get_graph_size()

        # Size of each cell
        self.CELL_SIZE = (self.SCREEN_WIDTH - 2 * self.MARGIN_SIZE) // self.N_CELLS

        # Size of the button
        self.BUTTON_THEME_SIZE = 50
        self.BUTTON_THEME_X = self.SCREEN_WIDTH - self.BUTTON_THEME_SIZE - 10
        self.BUTTON_THEME_Y = 4

        # Button icon
        self.ICON_THEME_SIZE = 20
        self.ICON_THEME_X = self.BUTTON_THEME_X + \
            (self.BUTTON_THEME_SIZE - self.ICON_THEME_SIZE) // 2
        self.ICON_THEME_Y = self.BUTTON_THEME_Y + \
            (self.BUTTON_THEME_SIZE - self.ICON_THEME_SIZE) // 2

        # Size of the check win button
        self.BUTTON_WIN_WIDTH = 100 # Increase this to make the button wider
        self.BUTTON_WIN_HEIGHT = 50
        self.BUTTON_WIN_X = 10
        self.BUTTON_WIN_Y = 8
        
        # Win status
        self.has_won = False
        # Button clicked status
        self.button_clicked = False
        
        # Create the data with the file
        self.circle_data = self.game.graph.create_circle_data(filename)

        self.prev_cell_clicked = (-10, -10)

    def draw(self, screen, events):
        """Draws the game on the screen

        Args:
            screen: screen to draw the game
            events: events to check if the user clicked on the theme button
        """
        screen.fill(self.colors.BLACK)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the theme button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.BUTTON_THEME_X <= mouse_x <= self.BUTTON_THEME_X + self.BUTTON_THEME_SIZE and \
                        self.BUTTON_THEME_Y <= mouse_y <= self.BUTTON_THEME_Y + self.BUTTON_THEME_SIZE:
                    self.colors.change_dark_mode()
                # Check if the mouse is over the check win button
                elif self.BUTTON_WIN_X <= mouse_x <= self.BUTTON_WIN_X + self.BUTTON_WIN_WIDTH and \
                        self.BUTTON_WIN_Y <= mouse_y <= self.BUTTON_WIN_Y + self.BUTTON_WIN_HEIGHT:
                    self.check_win()
                    
        if self.button_clicked:
            font = pygame.font.Font(None, 54)
            if self.has_won:
                text = font.render("You Win!", True, self.colors.GREEN)
            else:
                text = font.render("You have errors", True, self.colors.RED)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, 50))
            
            # Add a white background behind the text
            pygame.draw.rect(screen, self.colors.WHITE, (text_rect.x - 2,
                             text_rect.y - 2, text_rect.width + 10, text_rect.height + 10))
            screen.blit(text, text_rect)

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.drawn_lines, self.prev_cell_clicked = self.mc.detects_lines(
            mouse_buttons, mouse_pos, self.CELL_SIZE, self.MARGIN_SIZE, self.N_CELLS, self.prev_cell_clicked, self.drawn_lines)

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

        # Draw the check win button
        pygame.draw.rect(screen, self.colors.WHITE, (self.BUTTON_WIN_X,
                         self.BUTTON_WIN_Y, self.BUTTON_WIN_WIDTH, self.BUTTON_WIN_HEIGHT))
        font = pygame.font.Font(None, 24)
        text = font.render("Check Win", True, self.colors.BLACK)
        screen.blit(text, (self.BUTTON_WIN_X + 10, self.BUTTON_WIN_Y + 10))

    def check_win(self):
        print("///////////////////////////////////////////////////")
        print("Button clicked!")
        self.has_won = self.game.check_solved()
        self.button_clicked = True
        print(self.has_won)