class MouseController:
    """
    MouseController class to handle mouse interactions with the graph

    Attributes
    ----------
    graph : Graph
        The graph that the mouse controller interacts with

    Methods
    -------
    __init__(graph)
        Initialize the mouse controller with a graph
    check_cell_click(mouse_pos, cell_size, margin_size, N_CELLS)
        Check if the mouse click is inside the grid and return the position of the cell clicked
    is_adjacent(cell1, cell2)
        Check if the cell 1 and the cell 2 are adjacent
    is_line_exits(cell1, cell2, drawn_lines)
        Check if the line between cell1 and cell2 is already drawn
    delete_lines_like(cell1, cell2, drawn_lines)
        Delete the lines like cell1 and cell2
    delete_diagonal_lines(drawn_lines)
        Delete the diagonal lines
    delete_non_adjacent_lines(drawn_lines)
        Delete the non-adjacent lines
    detects_lines(mouse_buttons, mouse_pos, CELL_SIZE,
                  MARGIN_SIZE, N_CELLS, prev_cell_clicked, drawn_lines)
        Detects the lines drawn by the player
    """
    
    def __init__(self, game) -> None:
        self.game = game
        
    # Check if the mouse click is inside the grid and return the position of
    # the cell clicked
    def check_cell_click(self, mouse_pos, cell_size, margin_size, N_CELLS):
        """
        @param mouse_pos: tuple (x, y) with the position of the mouse
        @param cell_size: int with the size of the cell
        @param margin_size: int with the size of the margin
        @param N_CELLS: int with the number of cells in a row or column
    
        @return: tuple (row, col) with the position of the cell clicked
    
        Check if the mouse click is inside the grid and return the position of the cell clicked
        """
        # Calculate the grid position of the click
        mouse_x, mouse_y = mouse_pos
        grid_x = (mouse_x - margin_size) // cell_size
        grid_y = (mouse_y - margin_size) // cell_size
        # Check if the click is inside the grid
        if 0 <= grid_x < N_CELLS and 0 <= grid_y < N_CELLS:
            # Adding 1 to convert to 1-based indexing
            return grid_y + 1, grid_x + 1
        else:
            return None
    
    # Check if the cell 1 and the cell 2 are adjacent
    def is_adjacent(self, cell1, cell2):
        """
        @param cell1: tuple (row, col) with the position of the first cell
        @param cell2: tuple (row, col) with the position of the second cell
    
        @return: bool with the result of the comparison
    
        Check if the cell 1 and the cell 2 are adjacent
        """
    
        row1, col1 = cell1
        row2, col2 = cell2
    
        if row1 != -10 and col1 != -10 and row2 != -10 and col2 != -10:
            if (row1 == row2 and abs(col1 - col2) ==
                    1) or (col1 == col2 and abs(row1 - row2) == 1):
                return True
    
        return False
    
    # Check if the line between cell1 and cell2 is already drawn
    def is_line_exits(self, cell1, cell2, drawn_lines):
        """
        @param cell1: tuple (row, col) with the position of the first cell
        @param cell2: tuple (row, col) with the position of the second cell
        @param drawn_lines: list with the lines drawn
    
        @return: bool with the result of the comparison
    
        Check if the line between cell1 and cell2 is already drawn
        """
    
        pos_y1, pos_x1 = cell1
        pos_y2, pos_x2 = cell2
    
        for i in range(0, len(drawn_lines), 2):
            cell_start = drawn_lines[i]
            cell_finish = drawn_lines[i + 1]
            x1, y1 = cell_start
            x2, y2 = cell_finish
            if (pos_y1 == x1 and pos_x1 == y1 and pos_y2 == x2 and pos_x2 == y2) or (
                    pos_y1 == x2 and pos_x1 == y2 and pos_y2 == x1 and pos_x2 == y1):
                return True
    
        return False
    
    def delete_lines_like(self, cell1, cell2, drawn_lines):
        """
        @param cell1: tuple (row, col) with the position of the first cell
        @param cell2: tuple (row, col) with the position of the second cell
        @param drawn_lines: list with the lines drawn
    
        @return: list with the lines drawn without the lines like cell1 and cell2
    
        Delete the lines like cell1 and cell2
        """
    
        non_duplicate_lines = []
        for i in range(0, len(drawn_lines), 2):
            cell_start = drawn_lines[i]
            cell_finish = drawn_lines[i + 1]
            if (cell_start != cell1 or cell_finish != cell2) and (
                    cell_start != cell2 or cell_finish != cell1):
                non_duplicate_lines.append(cell_start)
                non_duplicate_lines.append(cell_finish)
    
        return non_duplicate_lines
    
    def delete_diagonal_lines(self, drawn_lines):
        """
        @param drawn_lines: list with the lines drawn
    
        @return: list with the lines drawn without the diagonal lines
    
        Delete the diagonal lines
        """
        non_diagonal_lines = []
    
        for i in range(1, len(drawn_lines), 2):
            cell_start = drawn_lines[i - 1]
            cell_finish = drawn_lines[i]
            x1, y1 = cell_start
            x2, y2 = cell_finish
            if abs(x1 - x2) != 1 or abs(y1 - y2) != 1:
                non_diagonal_lines.append(cell_start)
                non_diagonal_lines.append(cell_finish)
    
        return non_diagonal_lines
    
    # Delete the non-adjacent lines
    def delete_non_adjacent_lines(self, drawn_lines):
        """
        @param drawn_lines: list with the lines drawn
    
        @return: list with the lines drawn without the non-adjacent lines
    
        Delete the non-adjacent lines
        """
        adjacent_lines = []
    
        for i in range(0, len(drawn_lines), 2):
            cell_start = drawn_lines[i]
            cell_finish = drawn_lines[i + 1]
            x1, y1 = cell_start
            x2, y2 = cell_finish
    
            if abs(x1 - x2) + abs(y1 - y2) == 1:
                adjacent_lines.append(cell_start)
                adjacent_lines.append(cell_finish)
    
        return adjacent_lines
    
    # Detects the lines drawn by the player
    def detects_lines(
            self,
            mouse_buttons,
            mouse_pos,
            CELL_SIZE,
            MARGIN_SIZE,
            N_CELLS,
            prev_cell_clicked,
            drawn_lines):
        """
        @param mouse_buttons: list with the state of the mouse buttons
        @param mouse_pos: tuple (x, y)
        @param CELL_SIZE: int with the size of the cell
        @param MARGIN_SIZE: int with the size of the margin
        @param N_CELLS: int with the number of cells in a row or column
        @param prev_cell_clicked: tuple (row, col)
        @param drawn_lines: list with the lines drawn
    
        @return: tuple with the lines drawn and the previous cell clicked
    
        Detects the lines drawn by the player
        """
    
        if mouse_buttons[0]:  # The left mouse button is pressed
            cell_clicked = self.check_cell_click(
                mouse_pos, CELL_SIZE, MARGIN_SIZE, N_CELLS)
            if cell_clicked and cell_clicked != prev_cell_clicked:
                if self.is_adjacent(prev_cell_clicked, cell_clicked):
                    if (self.is_line_exits(prev_cell_clicked, cell_clicked, drawn_lines)):
                        print("removing")
                        print(prev_cell_clicked, cell_clicked)
                        s_x, s_y = prev_cell_clicked
                        e_x, e_y = cell_clicked
                        self.game.undo_move(s_x - 1, s_y - 1, e_x - 1, e_y - 1)
                        drawn_lines = self.delete_lines_like(
                            prev_cell_clicked, cell_clicked, drawn_lines)
                    else:
                        print("adding")
                        print(prev_cell_clicked, cell_clicked)
                        s_x, s_y = prev_cell_clicked
                        e_x, e_y = cell_clicked
                        self.game.make_move(
                            s_x - 1, s_y - 1, e_x - 1, e_y - 1)
                        drawn_lines.append(prev_cell_clicked)
                        drawn_lines.append(cell_clicked)
                    drawn_lines = self.delete_diagonal_lines(drawn_lines)
                    drawn_lines = self.delete_non_adjacent_lines(drawn_lines)
                prev_cell_clicked = cell_clicked
    
        return drawn_lines, prev_cell_clicked
    