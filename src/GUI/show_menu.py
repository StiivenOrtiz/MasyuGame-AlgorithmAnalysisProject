# import pygame
import pygame
import sys

import Util.colors as COLORS

from Util.read_files import select_file


class Menu:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.current_state = "menu"
        self.colors = COLORS.colors()
        self.filename = ""
        self.new_game = False

    # Function to show text on the screen
    def show_text(self, screen, text, x, y, color, size, isCenter):
        font = pygame.font.Font(None, size)
        rendered_text = font.render(text, True, color)
        if isCenter:
            screen.blit(rendered_text,
                        (x - (rendered_text.get_width() // 2),
                         y - (rendered_text.get_height() // 2)))
            rendered_text.get_height()
        else:
            screen.blit(rendered_text, (x, y))

    # Function to draw the menu
    def draw(self, screen, events, current_state, actual_filename):
        self.current_state = current_state
        screen.fill(self.colors.BLACK)
        
        # Show the title of the game
        title = "¡MASYU!"
        objetcts_pos_x = (self.SCREEN_WIDTH // 2)
        objetcts_pos_y = (self.SCREEN_HEIGHT // 2) - (self.SCREEN_HEIGHT // 5)
        
        self.show_text(screen, title, objetcts_pos_x, objetcts_pos_y, self.colors.WHITE, 128, True)

        # Get the mouse position and click
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        # Create the buttons
        button_width = 256
        button_height = 64
        interspersed = 2
        center_button_height = self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 2) - (button_height // 2)
        center_button_width = self.SCREEN_WIDTH - (self.SCREEN_WIDTH //2) - (button_width // 2)
        
        # Create the buttons
        continue_button = pygame.Rect(center_button_width, center_button_height + ((button_height * (0 * interspersed)) // 1.5), button_width, button_height)   
        new_game_button = pygame.Rect(center_button_width, center_button_height + ((button_height * (1 * interspersed)) // 1.5), button_width, button_height)
        ia_button = pygame.Rect(center_button_width, center_button_height + ((button_height * (2 * interspersed)) // 1.5), button_width, button_height)
        quit_button = pygame.Rect(center_button_width, center_button_height + ((button_height * (3 * interspersed)) // 1.5), button_width, button_height)

        # Draw the buttons
        pygame.draw.rect(screen, self.colors.WHITE, continue_button)
        pygame.draw.rect(screen, self.colors.WHITE, new_game_button)
        pygame.draw.rect(screen, self.colors.WHITE, ia_button)
        pygame.draw.rect(screen, self.colors.WHITE, quit_button)

        # Show the text of the buttons
        self.show_text(screen, "CONTINUE",
                       self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 2),
                       self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 2) + ((button_height * (0 * interspersed)) // 1.5),
                       self.colors.BLACK, 48, True)
        self.show_text(screen, "NEW GAME",
                       self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 2),
                       self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 2) + ((button_height * (1 * interspersed)) // 1.5),
                       self.colors.BLACK, 48, True)
        self.show_text(screen, "AI GAME",
                       self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 2),
                       self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 2) + ((button_height * (2 * interspersed)) // 1.5),
                       self.colors.BLACK, 48, True)
        self.show_text(screen, "QUIT",
                       self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 2),
                       self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 2) + ((button_height * (3 * interspersed)) // 1.5),
                       self.colors.BLACK, 48, True)

        # Check if the buttons are clicked to change the state of the game 
        if continue_button.collidepoint((mouse_x, mouse_y)) and click:
            if actual_filename != "":
                self.new_game = False
                self.filename = actual_filename
                self.current_state = "game"
            else:
                self.new_game = True
                self.filename = select_file()
                if self.filename is not None:
                    self.current_state = "game"
        elif new_game_button.collidepoint((mouse_x, mouse_y)) and click:
            self.new_game = True
            self.filename = select_file()
            if self.filename is not None:
                self.current_state = "game"
        elif ia_button.collidepoint((mouse_x, mouse_y)) and click:
            print("AI game")
        elif quit_button.collidepoint((mouse_x, mouse_y)) and click:
            pygame.quit()
            sys.exit()

        # Update the screen
        pygame.display.update()

        # Check if the user wants to quit the game
        for evento in events:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()