from Logic.node import Node


class Graph:
    """
    Graph class to represent a graph
    
    Attributes
    ----------
    adjacency_matrix : list
        The adjacency matrix of the graph
    size : int
        The size of the graph
    connected_nodes : list
        The list of connected nodes in the graph
    
    Methods
    -------
    create_adjacency_matrix(file_name)
        Create an adjacency matrix from a file
    create_circle_data(file_name)
        Create circle data from a file
    add_edge(s_x, s_y, e_x, e_y)
        Add an edge between two nodes
    remove_edge(s_x, s_y, e_x, e_y)
        Remove an edge between two nodes
    get_connected_nodes()
        Get all connected nodes in the graph
    remove_all_connected_nodes()
        Remove all connected nodes from the graph
    all_valid_connections()
        Check if all connections in the graph are valid
    check_win()
        Check if the game is over, this is when the graph is cyclic
    dfs(current_node, visited, parent_node)
        Depth-first search from a node
    is_cyclic()
        Check if the graph is cyclic
    check_valid_black(node)
        Check if a black node is valid
    check_valid_white(node)
        Check if a white node is valid
    check_adyacent_black(x, y)
        Check the adjacent black nodes of a node
    check_adyacent_white(x, y)
        Check the adjacent white nodes of a node
    print_connected_nodes()
        Print all connected nodes in the graph
    print_graph()
        Print the graph
    """

    def __init__(self, file_name) -> None:
        self.adjacency_matrix = self.create_adjacency_matrix(file_name)
        self.size = len(self.adjacency_matrix)
        self.connected_nodes = []
        self.pearls = self.get_pearls()

    def create_adjacency_matrix(self, file_name: str) -> list[list[Node]]:
        """Create an adjacency matrix from a file

        Args:
            file_name (str): The name of the file

        Returns:
            list[list[Node]]: The adjacency matrix
        """
        with open(file_name, 'r') as file:
            # Read the first line to get the dimensions of the matrix
            dimensions = int(file.readline().strip())

            adjacency_matrix = [[None for _ in range(
                dimensions)] for _ in range(dimensions)]

            # Read the rest of the file to fill the matrix
            for line in file:
                row, col, color = map(int, line.strip().split(','))
                # print(adjacency_matrix[row - 1][col - 1])
                adjacency_matrix[row - 1][col -
                                          1] = Node(color, row - 1, col - 1)
                # print(adjacency_matrix[row - 1][col - 1])

        # Fill the matrix with the spaces
        for i in range(dimensions):
            for j in range(dimensions):
                if adjacency_matrix[i][j] is None:
                    adjacency_matrix[i][j] = Node(None, i, j)

        return adjacency_matrix

    def create_circle_data(self, file_name: str) -> dict:
        """Create circle data from a file

        Args:
            file_name (str): The name of the file

        Returns:
            dict: The circle data
        """
        circle_data = {}
        with open(file_name, 'r') as file:
            # Skip the first line (dimensions)
            next(file)

            # Read the rest of the file to fill the dictionary
            for line in file:
                row, col, color = map(int, line.strip().split(','))
                circle_data[(row, col)] = color
        return circle_data

    def add_edge(self, s_x: int, s_y: int, e_x: int, e_y: int) -> None:
        """Add an edge between two nodes

        Args:
            s_x (int): start node x position
            s_y (int): start node y position
            e_x (int): end node x position
            e_y (int): end node y position
        """
        start_node = self.adjacency_matrix[s_x][s_y]
        end_node = self.adjacency_matrix[e_x][e_y]
        # print("adding")
        # print(start_node, end_node)

        # add weight
        end_node.weight += 1
        start_node.weight += 1

        # add node in the start node adjacent list
        start_node.add_adjacent_node(end_node)
        end_node.add_adjacent_node(start_node)

        # print()
        # print("Start node...")
        # print(f"Adjacent nodes of {start_node}:")
        # for node in start_node.adjacency_list:
        #     print(node, end= " ")
        # print()

        # print("End node...")
        # print(f"Adjacent nodes of {end_node}:")
        # for node in end_node.adjacency_list:
        #     print(node, end=" ")
        # print()

    def remove_edge(self, s_x: int, s_y: int, e_x: int, e_y: int) -> None:
        """Remove an edge between two nodes

        Args:
            s_x (int): start node x position
            s_y (int): start node y position
            e_x (int): end node x position
            e_y (int): end node y position
        """
        start_node = self.adjacency_matrix[s_x][s_y]
        end_node = self.adjacency_matrix[e_x][e_y]
        # print("removing")
        # print(start_node, end_node)
        # decrease weight
        end_node.weight -= 1
        start_node.weight -= 1

        # remove node from the start node adjacent list
        start_node.remove_adjacent_node(end_node)
        end_node.remove_adjacent_node(start_node)

    def get_connected_nodes(self):
        """get all connected nodes in the graph
        """
        for row in self.adjacency_matrix:
            for node in row:
                if node.list_size() > 0 and node not in self.connected_nodes:
                    self.connected_nodes.append(node)

    def get_pearls(self) -> list[Node]:
        """get all pearls in the graph
        """
        pearls = []
        for row in self.adjacency_matrix:
            for node in row:
                if node.color != None:
                    pearls.append(node)
        return pearls

    def remove_all_connected_nodes(self):
        """remove all connected nodes from the graph
        """
        self.connected_nodes.clear()

    def all_valid_connections(self) -> bool:
        """check if all connections in the graph are valid

        Returns:
            bool: True if all connections are valid, False otherwise
        """
        for row in self.adjacency_matrix:
            for node in row:
                if node.weight > 2:
                    return False
        return True

    def check_win(self) -> bool:
        """
        Check if the game is over, this is when the graph is cyclic
        """
        self.remove_all_connected_nodes()
        self.get_connected_nodes()
        self.print_connected_nodes()
        return self.is_cyclic()

    class InvalidNodeException(Exception):
        pass

    def dfs(self, current_node: Node, visited: list[Node], parent_node: Node, pearls_included: list[Node]) -> bool:
        """Do a depth-first search from a node to check if the graph is cyclic

        Args:
            current_node (Node): the current node
            visited (list[Node]): the list of visited nodes
            parent_node (Node): the parent node
            pearls_included (list[Node]): list of pearls included in the visited nodes

        Raises:
            Graph.InvalidNodeException: if an invalid node is found

        Returns:
            bool: True if a cycle is found and all pearls are included, False otherwise
        """
        print(f"Visiting node: {current_node}", current_node.color)
        visited.append(current_node)

        if current_node.color != None:
            pearls_included.append(current_node)

        # Validate the node based on its color
        if current_node.color == 1:  # White
            if not self.check_valid_white(current_node):
                print("Node is white, checking validity...")
                print("Node is not valid, raising InvalidNodeException")
                raise Graph.InvalidNodeException
            print("Node is valid")

        elif current_node.color == 2:  # Black
            if not self.check_valid_black(current_node):
                print("Node is black, checking validity...")
                print("Node is not valid, raising InvalidNodeException")
                raise Graph.InvalidNodeException
            print("Node is valid")

        for adjacent_node in current_node.adjacency_list:
            if adjacent_node not in visited:
                if self.dfs(adjacent_node, visited, current_node, pearls_included):
                    return True
            elif adjacent_node != parent_node:
                print("Found a cycle")
                if len(pearls_included) == len(self.pearls):
                    print("All pearls included, returning True")
                    return True
                else:
                    print("Not all pearls included, returning False")
                    return False

        return False

    def is_cyclic(self) -> bool:
        """Check if the graph is cyclic

        Returns:
            bool: True if the graph is cyclic, False otherwise
        """
        if not self.all_valid_connections():
            return False

        self.get_connected_nodes()

        if len(self.connected_nodes) == 0:
            return False

        node = self.connected_nodes[0]
        visited = []  # Clear the visited list for each new starting node
        pearls_included = []

        try:
            if self.dfs(node, visited, None, pearls_included):
                return True
            else:
                return False
        except Graph.InvalidNodeException:
            print("Invalid node found, stopping DFS")
            return False

    def check_valid_black(self, node: Node) -> bool:
        """check if the black node is valid or not

        Args:
            node (Node): the node to check

        Returns:
            bool: True if the node is valid, False otherwise
        """
        valid = False
        if self.check_adyacent_black(node.x, node.y):
            valid = True

        return valid

    def check_valid_white(self, node: Node) -> bool:
        """check if the white node is valid or not

        Args:
            node (Node): the node to check

        Returns:
            bool: True if the node is valid, False otherwise
        """
        valid = False
        # print("fasfda", self.adjacency_matrix[x][y].weight)
        if self.check_adyacent_white(node.x, node.y):
            valid = True
        return valid

    def check_adyacent_black(self, x: int, y: int) -> bool:
        """return in what positions are the two adyacent nodes that are connected to the node

        Args:
            x (int): the x position of the node
            y (int): the y position of the node

        Returns:
            bool: True if the node is valid, False otherwise
        """
        pos_adyacent = []
        # print(x + 1, y + 1, self.size)

        # check down
        if (0 <= (x + 1) <= (self.size - 2)):
            # print("check down")
            if (self.adjacency_matrix[x + 1][y].valid_connections()
                    and self.adjacency_matrix[x + 2][y].valid_connections()):
                pos_adyacent.append(1)

        # check left
        if (3 <= (y + 1) <= self.size):
            # print("check left")
            if (self.adjacency_matrix[x][y - 1].valid_connections()
                    and self.adjacency_matrix[x][y - 2].valid_connections()):
                pos_adyacent.append(2)

        # check right
        if (0 <= (y + 1) <= (self.size - 2)):
            # print("check right")
            if (self.adjacency_matrix[x][y + 1].valid_connections()
                and self.adjacency_matrix[x][y + 2].valid_connections()
                    and not 2 in pos_adyacent):
                pos_adyacent.append(3)

        # check up
        if (3 <= (x + 1) <= self.size):
            # print("check up")
            if (self.adjacency_matrix[x - 1][y].valid_connections()
                and self.adjacency_matrix[x - 2][y].valid_connections()
                    and not 1 in pos_adyacent):
                pos_adyacent.append(4)

        print(len(pos_adyacent))
        if len(pos_adyacent) == 2:
            return True
        return False

    def check_adyacent_white(self, x: int, y: int) -> bool:
        """return in what positions are the two adyacent nodes that are connected to the node

        Args:
            x (int): the x position of the node
            y (int): the y position of the node

        Returns:
            bool: True if the node is valid, False otherwise
        """
        in_column = False
        in_row = False
        first_row = False
        last_row = False
        first_col = False
        last_col = False
        # check an adyacent connection

        # if is on the first row
        # check left and right
        if (x == 0):
            # print("auida1")
            if (self.adjacency_matrix[x][y - 1].valid_connections()
                    and self.adjacency_matrix[x][y + 1].valid_connections()):
                first_row = True

        # if is on the last row
        # check left and right
        elif ((x + 1) == self.size):
            # print("auida2")
            if (self.adjacency_matrix[x][y - 1].valid_connections()
                    and self.adjacency_matrix[x][y + 1].valid_connections()):
                last_row = True

        # if is on the first column
        # check up and down
        elif (y == 0):
            # print("auida3")
            if (self.adjacency_matrix[x - 1][y].valid_connections()
                    and self.adjacency_matrix[x - 1][y].valid_connections()):
                first_col = True

        # if is on the last column
        # check up and down
        elif ((y + 1) == self.size):
            # print("auida4")
            if (self.adjacency_matrix[x - 1][y].valid_connections()
                    and self.adjacency_matrix[x - 1][y].valid_connections()):
                last_col = True

        else:

            # print(self.adjacency_matrix[x - 1][y].valid_connections(), self.adjacency_matrix[x + 1][y].valid_connections())
            if ((self.adjacency_matrix[x - 1][y].valid_connections()
                and self.adjacency_matrix[x - 1][y] in self.adjacency_matrix[x][y].adjacency_list)
                and (self.adjacency_matrix[x + 1][y].valid_connections()
                     and self.adjacency_matrix[x + 1][y] in self.adjacency_matrix[x][y].adjacency_list)):
                # print("in col")
                in_column = True

            elif ((self.adjacency_matrix[x][y - 1].valid_connections()
                   and self.adjacency_matrix[x][y - 1] in self.adjacency_matrix[x][y].adjacency_list)
                  and (self.adjacency_matrix[x][y + 1].valid_connections()
                       and self.adjacency_matrix[x][y + 1] in self.adjacency_matrix[x][y].adjacency_list)):
                # print("in row")
                in_row = True
            # print("validaciones")
            # print(in_column, in_row)
            if in_column == False and in_row == False:
                # print("entre aqui2")
                return False
        # check turns

        # if is on the first row
        if first_row:
            if ((self.adjacency_matrix[x + 1][y - 1].valid_connections()
                and self.adjacency_matrix[x + 1][y - 1] in self.adjacency_matrix[x][y - 1].adjacency_list)
                or (self.adjacency_matrix[x + 1][y + 1].valid_connections()
                    and self.adjacency_matrix[x + 1][y + 1] in self.adjacency_matrix[x][y + 1].adjacency_list)):
                return True
        # if is on the last row
        elif last_row:
            if ((self.adjacency_matrix[x - 1][y - 1].valid_connections()
                and self.adjacency_matrix[x - 1][y - 1] in self.adjacency_matrix[x][y - 1].adjacency_list)
                or (self.adjacency_matrix[x - 1][y + 1].valid_connections()
                    and self.adjacency_matrix[x - 1][y + 1] in self.adjacency_matrix[x][y + 1].adjacency_list)):
                return True
        # if is on the first column
        elif first_col:
            if ((self.adjacency_matrix[x - 1][y + 1].valid_connections()
                and self.adjacency_matrix[x - 1][y + 1] in self.adjacency_matrix[x - 1][y].adjacency_list)
                or (self.adjacency_matrix[x + 1][y + 1].valid_connections()
                    and self.adjacency_matrix[x + 1][y + 1] in self.adjacency_matrix[x + 1][y].adjacency_list)):
                return True
        # if is on the last column
        elif last_col:
            if ((self.adjacency_matrix[x - 1][y - 1].valid_connections()
                and self.adjacency_matrix[x - 1][y - 1] in self.adjacency_matrix[x - 1][y].adjacency_list)
                or (self.adjacency_matrix[x + 1][y - 1].valid_connections()
                    and self.adjacency_matrix[x + 1][y - 1] in self.adjacency_matrix[x + 1][y].adjacency_list)):
                return True

        # check turn
        elif in_column:
            # check connection turn to a column or row
            # check left
            # print(
            #     (self.adjacency_matrix[x - 1][y + 1],
            #     self.adjacency_matrix[x - 1][y + 1] in self.adjacency_matrix[x][y].adjacency_list))

            # x - 1
            if self.adjacency_matrix[x - 1][y - 1] in self.adjacency_matrix[x - 1][y].adjacency_list:
                return True
            elif self.adjacency_matrix[x - 1][y + 1] in self.adjacency_matrix[x - 1][y].adjacency_list:
                return True

            # x + 1
            elif self.adjacency_matrix[x + 1][y - 1] in self.adjacency_matrix[x + 1][y].adjacency_list:
                return True
            elif self.adjacency_matrix[x + 1][y + 1] in self.adjacency_matrix[x + 1][y].adjacency_list:
                return True

            # if ((self.adjacency_matrix[x - 1][y - 1].valid_connections()
            #     and self.adjacency_matrix[x - 1][y - 1] in self.adjacency_matrix[x][y].adjacency_list)
            #     or (self.adjacency_matrix[x + 1][y - 1].valid_connections()
            #     and self.adjacency_matrix[x + 1][y - 1] in self.adjacency_matrix[x][y].adjacency_list)
            #     or (self.adjacency_matrix[x - 1][y + 1].valid_connections()
            #     and self.adjacency_matrix[x - 1][y + 1] in self.adjacency_matrix[x][y].adjacency_list)
            #     or (self.adjacency_matrix[x + 1][y + 1].valid_connections()
            #     and self.adjacency_matrix[x + 1][y + 1] in self.adjacency_matrix[x][y].adjacency_list)):
            #     # print("entre aqui3")
            #     return True

        elif in_row:
            # y - 1
            if self.adjacency_matrix[x - 1][y - 1] in self.adjacency_matrix[x][y - 1].adjacency_list:
                return True
            elif self.adjacency_matrix[x + 1][y - 1] in self.adjacency_matrix[x][y - 1].adjacency_list:
                return True
            # y + 1
            elif self.adjacency_matrix[x - 1][y + 1] in self.adjacency_matrix[x][y + 1].adjacency_list:
                return True
            elif self.adjacency_matrix[x + 1][y + 1] in self.adjacency_matrix[x][y + 1].adjacency_list:
                return True

        return False

    def print_connected_nodes(self):
        print("----SEE CONNECTED NODES----")
        for node in self.connected_nodes:
            print(f"Adjacent nodes of {node}:", end=" ")
            for adjacent in node.adjacency_list:
                print(adjacent, end=" ")
            print()
        print()

    def print_graph(self):
        print("----SEE GRAPH----")
        for row in self.adjacency_matrix:
            for cell in row:
                print(f"Adjacent nodes of {cell}:", end=" ")
                for node in cell.adjacency_list:
                    print(node, end=" ")
                print()
            print()
    
    def solve(self) -> bool:
        for x in range(self.size):
            for y in range(self.size):
                if self.adjacency_matrix[x][y].color is not None:
                    if self.backtrack(x, y):
                        return True
        return False

    def backtrack(self, x: int, y: int) -> bool:
        if x == self.size:
            return True

        nx, ny = (x, y + 1) if y + 1 < self.size else (x + 1, 0)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                self.add_edge(x, y, nx, ny)
                if self.is_cyclic():
                    if self.backtrack(nx, ny):
                        return True
                self.remove_edge(x, y, nx, ny)
        return False