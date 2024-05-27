from Logic.graph import Graph

class Game_flow:
    def __init__(self, filename) -> None:
        self.graph = Graph(filename)
    
    def make_move(self, s_x, s_y, e_x, e_y):
        """
        Make a move in the game
        """
        self.graph.add_edge(s_x, s_y, e_x, e_y)
        
    def undo_move(self, s_x, s_y, e_x, e_y):
        """
        Undo a move in the game
        """
        self.graph.remove_edge(s_x, s_y, e_x, e_y)
    
    def check_solved(self):
        """
        Check if the game is won
        """
        return self.graph.check_win()
    
    def get_graph_size(self):
        """
        Get the size of the graph
        """
        return self.graph.size