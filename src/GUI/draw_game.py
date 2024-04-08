# Imports
import pygame

# Draw the game

def drawAll(
        screen,
        N_CELLS,
        CELL_SIZE,
        MARGIN_SIZE,
        BUTTON_THEME_SIZE,
        BUTTON_THEME_X,
        BUTTON_THEME_Y,
        ICON_THEME_SIZE,
        ICON_THEME_X,
        ICON_THEME_Y,
        circle_data,
        drawn_lines,
        colors):
    drawButtonTheme(
        screen,
        BUTTON_THEME_SIZE,
        BUTTON_THEME_X,
        BUTTON_THEME_Y,
        ICON_THEME_SIZE,
        ICON_THEME_X,
        ICON_THEME_Y,
        colors)
    drawStructure(
        screen,
        N_CELLS,
        CELL_SIZE,
        MARGIN_SIZE,
        circle_data,
        drawn_lines,
        colors)

# Draw the button theme


def drawButtonTheme(
        screen,
        BUTTON_THEME_SIZE,
        BUTTON_THEME_X,
        BUTTON_THEME_Y,
        ICON_THEME_SIZE,
        ICON_THEME_X,
        ICON_THEME_Y,
        colors):
    # Draw the button theme
    pygame.draw.rect(
        screen,
        colors.WHITE,
        (BUTTON_THEME_X,
         BUTTON_THEME_Y,
         BUTTON_THEME_SIZE,
         BUTTON_THEME_SIZE))
    # Draw the icon theme
    pygame.draw.rect(
        screen,
        colors.BLACK,
        (ICON_THEME_X,
         ICON_THEME_Y,
         ICON_THEME_SIZE,
         ICON_THEME_SIZE))

# Draw the structure of the game


def drawStructure(
        screen,
        N_CELLS,
        CELL_SIZE,
        MARGIN_SIZE,
        circle_data,
        drawn_lines,
        colors):
    # Draw the grid
    for row in range(1, N_CELLS + 1):
        for col in range(1, N_CELLS + 1):
            x = (col - 1) * CELL_SIZE + MARGIN_SIZE
            y = (row - 1) * CELL_SIZE + MARGIN_SIZE
            # Draw the cell
            pygame.draw.rect(
                screen, colors.WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            # Draw the border of the cell
            pygame.draw.rect(
                screen, colors.BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # Draw the circles and lines
    for i in range(1, len(drawn_lines), 2):
        cell_start = drawn_lines[i - 1]
        cell_finish = drawn_lines[i]
        # print(f"\n[{i}]: Celda inicio: {cell_start}, Celda final: {cell_finish}")
        x1 = (cell_start[1] - 1) * CELL_SIZE + MARGIN_SIZE + CELL_SIZE // 2
        y1 = (cell_start[0] - 1) * CELL_SIZE + MARGIN_SIZE + CELL_SIZE // 2
        x2 = (cell_finish[1] - 1) * CELL_SIZE + MARGIN_SIZE + CELL_SIZE // 2
        y2 = (cell_finish[0] - 1) * CELL_SIZE + MARGIN_SIZE + CELL_SIZE // 2
        pygame.draw.line(screen, colors.BLACK, (x1, y1),
                         (x2, y2), CELL_SIZE // 6)

    # Draw the circles
    for row in range(1, N_CELLS + 1):
        for col in range(1, N_CELLS + 1):
            x = (col - 1) * CELL_SIZE + MARGIN_SIZE
            y = (row - 1) * CELL_SIZE + MARGIN_SIZE
            # Calculate the center of the cell
            half_x = x + CELL_SIZE // 2
            half_y = y + CELL_SIZE // 2

            if (row, col) in circle_data:
                circle_type = circle_data[(row, col)]
                if circle_type == 1:
                    # Draw a white circle
                    pygame.draw.circle(
                        screen, colors.WHITE, (half_x, half_y), (CELL_SIZE // 2.5))
                    # Draw a black circle
                    pygame.draw.circle(
                        screen, colors.BLACK, (half_x, half_y), (CELL_SIZE // 2.5), 10)
                elif circle_type == 2:
                    pygame.draw.circle(
                        screen, colors.BLACK, (half_x, half_y), (CELL_SIZE // 2.5))
            else:
                # Draw a black circle
                pygame.draw.circle(
                    screen, colors.BLACK, (half_x, half_y), (CELL_SIZE // 20))
