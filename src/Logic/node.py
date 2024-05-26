from typing import Optional


class Node:
    """
    Node class to represent a node in the graph

    Parameters
    ----------
    color : Optional[int]
        The color of the node
        1 = white
        2 = black
        None = empty
    value : int
        The weight of the node (default is 0), to know the connections of the node
    left : False
        If the node has a connection to the left
    right : False
        If the node has a connection to the right
    up : False
        If the node has a connection to the up
    down : False
        If the node has a connection to the down

    Methods
    -------
    valid_connections()
        Check if the node has more than two connections
    add_adjacent_node(node)
        Add a node to the adjacency list
    remove_adjacent_node(node)
        Remove a node from the adjacency list
    """
    def __init__(self, color: Optional[int], x: int, y: int) -> None:
        """
        Args:
            color (Optional[int]): The color of the node
            1: White
            2: Black
        """
        self.x = x
        self.y = y
        self.color = color
        self.weight = 0
        self.adjacency_list = []

    def valid_connections(self) -> bool:
        """Check if the node has more than two connections

        Returns:
            bool: _description_
        """
        if 0 < self.weight < 3:
            return True
        return False
    
    def add_adjacent_node(self, node) -> bool:
        """Add a node to the adjacency list

        Args:
            node (Node): The node to add

        Returns:
            bool: True if the node was added, False otherwise
        """
        return self.adjacency_list.append(node)
    
    def remove_adjacent_node(self, node) -> None:
        if node in self.adjacency_list:
            self.adjacency_list.remove(node)
            
    def list_size(self) -> int:
        """get the size of the adjacency list

        Returns:
            int: The size of the adjacency list
        """
        return len(self.adjacency_list)
        
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"