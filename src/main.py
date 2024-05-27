# imports
import pygame
import sys
import time
import Util.colors as COLORS
import GUI.show_game as show_game
import GUI.show_menu as show_menu
import Util.check_args as c_a

def main():
    # Check command line arguments
    filename, resolution = c_a.check_args(sys.argv)
    
    # Initialize the game
    pygame.init()

    # Define constants
    SCREEN_WIDTH = 426
    SCREEN_HEIGHT = 426

    if resolution > 200:
        SCREEN_WIDTH = resolution
        SCREEN_HEIGHT = resolution
        
    # Frames per second
    FPS = 60

    # Current state of the game
    current_state = "menu"

    # Initialize the game objects
    if filename != "" or filename != None:
        game = show_game.Game(SCREEN_WIDTH, SCREEN_HEIGHT, filename)
    
    menu = show_menu.Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    colors = COLORS.colors()

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Masyu")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Cambiar entre menú y juego
                if current_state == "menu":
                    current_state = "game"
                elif current_state == "game":
                    current_state = "menu"

        screen.fill(colors.BLACK)

        # Draw the current state
        if current_state == "menu":
            menu.draw(screen, events, current_state, filename)
            current_state = menu.current_state
            
            new_filename = menu.filename
            is_new_game = menu.new_game
            
            if new_filename != filename and is_new_game:
                filename = new_filename
                game = show_game.Game(SCREEN_WIDTH, SCREEN_HEIGHT, filename)
                
        elif current_state == "game":
            game.ai_game = False
            game.draw(screen, events)
        elif current_state == "ai_game":
            game.ai_game = True
            game.draw(screen, events)

        # Update the screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()