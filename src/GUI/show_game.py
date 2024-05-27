import pygame
import time
import Util.colors as COLORS
import GUI.draw_game as draw_game
from Controllers.mouse_controller import MouseController
from Logic.game import Game_flow


class Game:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, filename):
        self.state = "START"
        
        
        # List to store the drawn lines
        self.drawn_lines = []
        self.filename = filename
        self.ai_game = False
        self.ai_move_stack = []
        self.game_over = False  # Flag to indicate if the game is over
        
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
                print(self.game.graph.print_graph())
                time.sleep(60)
            else:
                text = font.render("You have errors", True, self.colors.RED)
            text_rect = text.get_rect(center=(self.SCREEN_WIDTH / 2, 50))
            
            # Add a white background behind the text
            pygame.draw.rect(screen, self.colors.WHITE, (text_rect.x - 2,
                             text_rect.y - 2, text_rect.width + 10, text_rect.height + 10))
            screen.blit(text, text_rect)
        
        if not self.ai_game:
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.drawn_lines, self.prev_cell_clicked = self.mc.detects_lines(
                mouse_buttons, mouse_pos, self.CELL_SIZE, self.MARGIN_SIZE, self.N_CELLS, self.prev_cell_clicked, self.drawn_lines)
            print("---------Drawn lines---------")
            print(self.drawn_lines)
            print ("-----------------------------")
        else:
            
            if self.state == "START":
            
                # play, x_n, y_n = self.game.graph.solve_mayus_game()
                
                #(first_black_pearl.x + 1, first_black_pearl.y + 1), black_return, (first_white_pearl.x + 1, first_white_pearl.y + 1), white_return
                
                black_cord, black_return, white_cord, white_return = self.game.graph.solve_mayus_game()
                
                print(f"Black: {black_cord} - {black_return}")
                print(f"White: {white_cord} - {white_return}")
                
                new_play_black = self.get_black_draw_connection(black_cord, black_return)
                new_play_white = self.get_white_draw_connection(white_cord, white_return)
                
                print(f"New play black: {new_play_black}")
                print(f"New play white: {new_play_white}")
                
                for i in range(0, len(new_play_black), 2):
                    self.make_ai_move(new_play_black[i][0], new_play_black[i][1], new_play_black[i + 1][0], new_play_black[i + 1][1])
                
                print(f"Drawn lines: {self.drawn_lines}")
                    
                n_new_play_white = self.game.graph.clean_list(new_play_white)
                
                print(f"New play white: {n_new_play_white}")
                
                for i in range(0, len(n_new_play_white), 2):
                    self.make_ai_move(n_new_play_white[i][0], n_new_play_white[i][1], n_new_play_white[i + 1][0], n_new_play_white[i + 1][1])
                
                print(f"Drawn lines: {self.drawn_lines}")
                
                self.state = "PLAY"

            
            
            
            
            # self.draw_all_game(screen)
            
            # # Solve the game
            # if not self.game_over:
            #     if self.solve_masyu(screen):
            #         self.game_over = True
            #         print("Game Over")
                
        # Draw the check win button
        self.draw_all_game(screen)
        pygame.draw.rect(screen, self.colors.WHITE, (self.BUTTON_WIN_X,
                         self.BUTTON_WIN_Y, self.BUTTON_WIN_WIDTH, self.BUTTON_WIN_HEIGHT))
        font = pygame.font.Font(None, 24)
        text = font.render("Check Win", True, self.colors.BLACK)
        screen.blit(text, (self.BUTTON_WIN_X + 10, self.BUTTON_WIN_Y + 10))

    def check_win(self):
        self.has_won = self.game.check_solved()
        self.button_clicked = True
        print(self.has_won)
        
    # Funcionees para la IA - NUEVO
    def get_black_draw_connection(self, origin, play):
        connection_list = []
        connection_list.extend([play[0], play[1], play[1], origin, origin, play[2], play[2], play[3]])
        return connection_list
    
    def get_white_draw_connection(self, origin, play):
        connection_list = []
        connection_list.extend([play[0], origin, origin, play[1], play[1], play[2]])
        return connection_list   
    
    
    
    # FIN funciones para la IA - NUEVO
        
    ## NUEVO
    
    # def solve_masyu(self, screen):
    #     if not self.backtrack(screen):
    #         print("No solution found")
    #         return False
    #     else:
    #         print("Solution found")
    #         return True
            
    # def backtrack(self, screen):
    #     if self.game.check_solved():
    #         return True

    #     if self.game.graph.first_random_move():
    #         print("First random move")
    #         possible_moves = self.game.graph.get_first_random_move()
            
    #     else:
    #         print("Possible moves")
    #         possible_moves = self.game.graph.get_possible_moves()

    #     for move in possible_moves:
    #         s_x, s_y, e_x, e_y = move
    #         self.make_ai_move(s_x + 1, s_y + 1, e_x + 1, e_y + 1)
    #         self.draw_all_game(screen)
    #         pygame.display.flip()  # Ensure the screen updates
    #         pygame.time.delay(10)  # Add a short delay to visualize moves
    #         if self.backtrack(screen):
    #             return True
    #         self.undo_ai_move()
    #         self.draw_all_game(screen)
    #         pygame.display.flip()  # Ensure the screen updates
    #         pygame.time.delay(10)  # Add a short delay to visualize moves
    #         return True
    #     return False

    def make_ai_move(self, s_x, s_y, e_x, e_y):
        self.game.make_move(s_x - 1, s_y - 1, e_x - 1, e_y - 1)
        self.drawn_lines.append((s_x, s_y))
        self.drawn_lines.append((e_x, e_y))
        self.ai_move_stack.append((s_x, s_y, e_x, e_y))  # Push move onto stack
        print("AI move made")

    def undo_ai_move(self):
        s_x, s_y, e_x, e_y = self.ai_move_stack.pop()  # Pop move from stack
        self.game.undo_move(s_x - 1, s_y - 1, e_x - 1, e_y - 1)
        self.drawn_lines = self.mc.delete_lines_like((s_x, s_y), (e_x, e_y), self.drawn_lines)
        print("AI move undone")
        
    ## FIN NUEVO
        
    # Draw game
    def draw_all_game(self, screen):
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