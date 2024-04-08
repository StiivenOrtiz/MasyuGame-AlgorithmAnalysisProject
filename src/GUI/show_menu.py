# import pygame
import pygame
import sys

import Util.colors as COLORS


class Menu:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.current_state = "menu"

        self.colors = COLORS.colors()

    # Function to show text on the screen

    def show_text(self, screen, text, x, y, color, size, isCenter):
        font = pygame.font.Font(None, size)
        rendered_text = font.render(text, True, color)
        if isCenter:
            screen.blit(rendered_text,
                        (x - (rendered_text.get_width() // 2),
                         y - (rendered_text.get_height() // 2)))
        else:
            screen.blit(rendered_text, (x, y))

    # Function to draw the menu
    def draw(self, screen, events, current_state):
        self.current_state = current_state
        screen.fill(self.colors.BLACK)
        # Show the title of the game
        self.show_text(screen,
                       "¡MASYU!",
                       (self.SCREEN_WIDTH // 2),
                       (self.SCREEN_HEIGHT // 2) - (self.SCREEN_HEIGHT // 6),
                       self.colors.WHITE,
                       128,
                       True)

        # Get the mouse position and click
        mouse_x, mouse_y = pygame.mouse.get_pos()
        click, _, _ = pygame.mouse.get_pressed()

        # Create the buttons
        button_width = 256
        button_height = 64

        start_button = pygame.Rect(self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 2) - (button_width // 2), self.SCREEN_HEIGHT - (
            self.SCREEN_HEIGHT // 2) - (button_height // 2) + ((button_height * (-1)) // 1.5), button_width, button_height)
        ia_button = pygame.Rect(self.SCREEN_WIDTH -
                                (self.SCREEN_WIDTH //
                                 2) -
                                (button_width //
                                 2), self.SCREEN_HEIGHT -
                                (self.SCREEN_HEIGHT //
                                    2) -
                                (button_height //
                                    2) +
                                ((button_height *
                                  1) //
                                    1.5), button_width, button_height)
        quit_button = pygame.Rect(self.SCREEN_WIDTH -
                                  (self.SCREEN_WIDTH //
                                   2) -
                                  (button_width //
                                   2), self.SCREEN_HEIGHT -
                                  (self.SCREEN_HEIGHT //
                                      2) -
                                  (button_height //
                                      2) +
                                  ((button_height *
                                    3) //
                                      1.5), button_width, button_height)

        # Draw the buttons
        pygame.draw.rect(screen, self.colors.WHITE, start_button)
        pygame.draw.rect(screen, self.colors.WHITE, ia_button)
        pygame.draw.rect(screen, self.colors.WHITE, quit_button)

        # Show the text of the buttons
        self.show_text(screen,
                       "START GAME",
                       self.SCREEN_WIDTH - (self.SCREEN_WIDTH // 2),
                       self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT // 2) + ((button_height * (-1)) // 1.5),
                       self.colors.BLACK,
                       48,
                       True)
        self.show_text(screen, "AI GAME", self.SCREEN_WIDTH -
                       (self.SCREEN_WIDTH //
                        2), self.SCREEN_HEIGHT -
                       (self.SCREEN_HEIGHT //
                        2) +
                       ((button_height *
                         1) //
                           1.5), self.colors.BLACK, 48, True)
        self.show_text(screen, "QUIT", self.SCREEN_WIDTH -
                       (self.SCREEN_WIDTH //
                        2), self.SCREEN_HEIGHT -
                       (self.SCREEN_HEIGHT //
                        2) +
                       ((button_height *
                         3) //
                           1.5), self.colors.BLACK, 48, True)

        # Check if the buttons are clicked
        if start_button.collidepoint((mouse_x, mouse_y)) and click:
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
