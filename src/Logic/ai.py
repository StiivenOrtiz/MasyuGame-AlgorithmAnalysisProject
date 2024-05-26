from graph import Graph

class AI:
    """AI class to solve the board using the graph
    """
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
        
    def solve(self) -> bool:
        """Solve the board using the graph

        Returns:
            bool: True if the board is solved, False otherwise
        """
        # Get the start and end nodes
        start_node = self.graph.start_node
        end_node = self.graph.end_node
        
        return False