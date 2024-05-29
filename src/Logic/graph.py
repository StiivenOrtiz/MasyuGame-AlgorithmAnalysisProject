from Logic.node import Node
import sys
sys.setrecursionlimit(10**6)


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
        
        if end_node not in start_node.adjacency_list and start_node not in end_node.adjacency_list:
            # add weight
            end_node.weight += 1
            start_node.weight += 1

            # add node in the start node adjacent list
            start_node.add_adjacent_node(end_node)
            end_node.add_adjacent_node(start_node)

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
        
        if end_node not in start_node.adjacency_list or start_node not in end_node.adjacency_list:
            return
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
        if node.color == 2:
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
        if node.color == 1:
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

        # print(len(pos_adyacent))
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
            # print("No se que esta pasando")
            # print(x, y, self.adjacency_matrix[x][y - 1].valid_connections(), self.adjacency_matrix[x][y + 1].valid_connections())
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
    
    def exist_connection(self, s_x: int, s_y: int, e_x: int, e_y: int) -> bool:
        """Check if an edge exists between two nodes

        Args:
            s_x (int): start node x position
            s_y (int): start node y position
            e_x (int): end node x position
            e_y (int): end node y position

        Returns:
            bool: True if the edge exists, False otherwise
        """
        start_node = self.adjacency_matrix[s_x][s_y]
        end_node = self.adjacency_matrix[e_x][e_y]
        return end_node in start_node.adjacency_list or start_node in end_node.adjacency_list

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
            
    def clean_list(self, return_list: list[tuple]) -> None:
        """Remove connections to the white pearls that already have two connections

        Args:
            return_list (list[tuple]): The list of white pearls
        """
        
        filtered_list = []
        
        # Iteramos sobre la lista en pasos de 2
        for i in range(0, len(return_list) - 1, 2):
            s_x, s_y = return_list[i][0] - 1, return_list[i][1] - 1
            e_x, e_y = return_list[i + 1][0] - 1, return_list[i + 1][1] - 1
            
            start_node = self.adjacency_matrix[s_x][s_y]
            end_node = self.adjacency_matrix[e_x][e_y]
            
            # Si las conexiones no están duplicadas, añadimos ambos puntos a la lista filtrada
            if end_node not in start_node.adjacency_list and start_node not in end_node.adjacency_list:
                filtered_list.append(return_list[i])
                filtered_list.append(return_list[i + 1])
        
        return filtered_list
            
    def get_classify_pearls(self):
        white_pearls = []
        black_pearls = []
        for pearl in self.pearls:
            if pearl.color == 1:
                white_pearls.append(pearl)
            elif pearl.color == 2:
                black_pearls.append(pearl)
        return black_pearls, white_pearls
    
    def get_possible_black_pearl_moves(self, pearl):
        moves = []
        row, col = pearl.x, pearl.y
        size = self.size

        # Direcciones para movimientos posibles
        directions = [
            ((0, -2), (0, -1), (1, 0), (2, 0)), # derecha y abajo
            ((0, -2), (0, -1), (-1, 0), (-2, 0)), # derecha y arriba
            ((0, 2), (0, 1), (1, 0), (2, 0)), # izquierda y abajo
            ((0, 2), (0, 1), (-1, 0), (-2, 0)), # izquierda y arriba
        ]

        for direction in directions:
            move = [(row + dr, col + dc) for dr, dc in direction]
            
            if all(0 <= r < size and 0 <= c < size for r, c in move):
                black_adjacent = False
                for i in range(len(move)):
                    if self.adjacency_matrix[move[i][0]][move[i][1]].color == 2 and \
                        ((row - 1 == move[i][0] and col == move[i][1]) or \
                         (row + 1 == move[i][0] and col == move[i][1]) or \
                         (row == move[i][0] and col - 1 == move[i][1]) or \
                         (row == move[i][0] and col + 1 == move[i][1])):
                        black_adjacent = True
                        break
                if black_adjacent == False:
                    moves.append(move)

        return moves
    
    def get_possible_white_pearl_moves(self, pearl):
        moves = []
        row, col = pearl.x, pearl.y
        size = self.size
        
        # Direcciones para movimientos posibles
        directions = [
            ((1, 0), (-1, 0), (-1, 1)), # Arriba y derecha
            ((1, 0), (-1, 0), (-1, -1)), # Arriba y izquierda
            ((-1, 0), (1, 0), (1, 1)), # Abajo y derecha
            ((-1, 0), (1, 0), (1, -1)), # Abajo y izquierda
            ((0, -1), (0, 1), (1, 1)), # Derecha y abajo
            ((0, -1), (0, 1), (-1, 1)), # Derecha y arriba
            ((0, 1), (0, -1), (1, -1)), # Izquierda y abajo
            ((0, 1), (0, -1), (-1, -1)), # Izquierda y arriba
        ]

        for direction in directions:
            move = [(row + dr, col + dc) for dr, dc in direction]
            if all(0 <= r < size and 0 <= c < size for r, c in move):
                moves.append(move)

        return moves
    
    def solve_mayus_game(self):
        black_pearls, white_pearls = self.get_classify_pearls()
        
        #diccionario de movimientos
        moves = {}
        
        for pearl in black_pearls:
            moves[(pearl.x, pearl.y)] = self.get_possible_black_pearl_moves(pearl)
        
        for pearl in white_pearls:
            moves[(pearl.x, pearl.y)] = self.get_possible_white_pearl_moves(pearl)
            
        return self.solve(moves, 1)
        
            
    def solve(self, moves, state):
        if len(moves) > 0:
            # Ordenar el diccionario de movimientos por la cantidad de movimientos posibles
            moves = dict(sorted(moves.items(), key=lambda item: len(item[1])))
            plays = {}
            # Si el primer elemento del diccionario tiene 1 movimiento posible, lo seleccionamos
            if len(moves[list(moves.keys())[0]]) == 1:
                for key in moves:
                    if len(moves[key]) == 1:
                        plays[key] = moves[key]
                    else:
                        break

                for key in plays:
                    del moves[key]
            else:
                key = list(moves.keys())[0]
                plays[key] = moves[key]
                del moves[key]

            for key in plays:
                for i in range(len(plays[key])):
                    move = plays[key][i]
                    plays_list = []
                    if self.adjacency_matrix[key[0]][key[1]].color == 1:
                        plays_list = [move[0], key, move[1], move[2]]
                    elif self.adjacency_matrix[key[0]][key[1]].color == 2:
                        plays_list = [move[0], move[1], key, move[2], move[3]]

                    print(f"\nMake play: {plays_list}")

                    for i in range(0, len(plays_list) - 1):
                        print("Adding edge", plays_list[i][0], plays_list[i][1], plays_list[i + 1][0], plays_list[i + 1][1])
                        self.add_edge(plays_list[i][0], plays_list[i][1], plays_list[i + 1][0], plays_list[i + 1][1])

                    new_moves = self.validate_new_moves(moves)
                    result = self.solve(new_moves, state + 1)

                    if result is not None:
                        return result

                    for i in range(0, len(plays_list) - 1):
                        print("Removing edge", plays_list[i][0], plays_list[i][1], plays_list[i + 1][0], plays_list[i + 1][1])
                        self.remove_edge(plays_list[i][0], plays_list[i][1], plays_list[i + 1][0], plays_list[i + 1][1])
        else:
            print("No more moves")

            print("Checking win ", self.check_win())
            if self.check_win():
                return self.return_draw_lines()

            free_cells = self.get_free_cells()

            if len(free_cells) == 0:
                return None

            for cell in free_cells:
                possible_connections = self.get_possible_connections(cell)
                for connection in possible_connections:

                    self.add_edge(cell[0], cell[1], connection[0], connection[1])
                    result = self.solve({}, state + 1)

                    if result is not None:
                        return result

                    self.remove_edge(cell[0], cell[1], connection[0], connection[1])

        

        
    def get_free_cells(self):
        # obtener las celdas que tengan 0 y 1 conexiones
        weight = []
        free_cells = []
        for row in self.adjacency_matrix:
            for cell in row:
                if cell.weight < 2:
                    free_cells.append((cell.x, cell.y))
                    weight.append(cell.weight)
                    
        #ordenar por peso (mayor a menor)
        free_cells = [x for _, x in sorted(zip(weight, free_cells), key=lambda pair: pair[0], reverse=True)]
                    
        return free_cells
    
    def get_possible_connections(self, node_):
        adj = [
            (-1, 0),  # up
            (0, -1),  # left
            (0, 1),   # right
            (1, 0),   # down
        ]
        
        return self.get_coords_nodes(node_, adj)
                    
    def return_draw_lines(self):
        self.remove_all_connected_nodes()
        self.get_connected_nodes()
        draw_lines = []
        for node in self.connected_nodes:
            for adjacent in node.adjacency_list:
                if not self.exist_in_drawn_lines((node.x + 1, node.y + 1), (adjacent.x + 1, adjacent.y + 1), draw_lines):
                    draw_lines.append((node.x + 1, node.y + 1))
                    draw_lines.append((adjacent.x + 1, adjacent.y + 1))          
        
        return draw_lines

    def exist_in_drawn_lines(self, cell1, cell2, drawn_lines):
        for i in range(0, len(drawn_lines) - 1, 2):  # iterate in steps of 2
            if (cell1 == drawn_lines[i] and cell2 == drawn_lines[i + 1]) or (cell1 == drawn_lines[i + 1] and cell2 == drawn_lines[i]):
                return True
        return False

    def valido_imprimir(self):
        count = 0
        
        print("\n1, 0 -> 1, 1 ", self.exist_connection(1, 0, 1, 1))
        print("1, 1 -> 1, 2 ", self.exist_connection(1, 0, 1, 1))
        print("1, 0 -> 2, 0 ", self.exist_connection(1, 0, 2, 0))
        print("2, 0 -> 3, 0 ", self.exist_connection(2, 0, 3, 0))
        print("3, 0 -> 4, 0 ", self.exist_connection(3, 0, 4, 0))
        print("4, 0 -> 5, 0 ", self.exist_connection(4, 0, 5, 0))
        print("5, 0 -> 5, 1 ", self.exist_connection(5, 0, 5, 1))
        print("2, 1 -> 3, 1 ", self.exist_connection(2, 1, 3, 1))
        print("3, 1 -> 4, 1 ", self.exist_connection(3, 1, 4, 1))
        print("4, 1 -> 4, 2 ", self.exist_connection(4, 1, 4, 2))
        print("4, 2 -> 4, 3 ", self.exist_connection(4, 2, 4, 3))
        print("4, 3 -> 4, 4 ", self.exist_connection(4, 3, 4, 4))
        print("4, 4 -> 3, 4 ", self.exist_connection(4, 4, 3, 4))
        print("3, 4 -> 2, 4 ", self.exist_connection(3, 4, 2, 4))
        print("2, 5 -> 1, 5 ", self.exist_connection(2, 5, 1, 5))
        print("1, 5 -> 0, 5 ", self.exist_connection(1, 5, 0, 5))
        print("0, 5 -> 0, 4 ", self.exist_connection(0, 5, 0, 4))
        print("0, 4 -> 0, 3 ", self.exist_connection(0, 4, 0, 3))
        print("0, 3 -> 1, 3 ", self.exist_connection(0, 3, 1, 3))
        print("1, 3 -> 2, 3 ", self.exist_connection(1, 3, 2, 3))
        print("1, 2 -> 1, 3 ", self.exist_connection(1, 2, 1, 3))
        
        if self.exist_connection(1, 0, 1, 1):
            count += 1
        if self.exist_connection(1, 1, 1, 2):
            count += 1
        if self.exist_connection(1, 0, 2, 0):
            count += 1
        if self.exist_connection(2, 0, 3, 0):
            count += 1
        if self.exist_connection(3, 0, 4, 0):
            count += 1
        if self.exist_connection(4, 0, 5, 0):
            count += 1
        if self.exist_connection(5, 0, 5, 1):
            count += 1
        if self.exist_connection(2, 1, 3, 1):
            count += 1
        if self.exist_connection(3, 1, 4, 1):
            count += 1
        if self.exist_connection(4, 1, 4, 2):
            count += 1
        if self.exist_connection(4, 2, 4, 3):
            count += 1
        if self.exist_connection(4, 3, 4, 4):
            count += 1
        if self.exist_connection(4, 4, 3, 4):
            count += 1
        if self.exist_connection(3, 4, 2, 4):
            count += 1
        if self.exist_connection(2, 5, 1, 5):
            count += 1
        if self.exist_connection(1, 5, 0, 5):
            count += 1
        if self.exist_connection(0, 5, 0, 4):
            count += 1
        if self.exist_connection(0, 4, 0, 3):
            count += 1
        if self.exist_connection(0, 3, 1, 3):
            count += 1
        if self.exist_connection(1, 3, 2, 3):
            count += 1
        
        
        print(f"\nCANTIDAD DE VALIDACIONES: {count}")
        
        return count
                                
    def validate_new_moves(self, moves):
        uptaded_moves = {}
        for key in moves:      
            print (f"\nKey: {key}")
            already_exists = self.already_exists(moves, key)
            
            if len(already_exists) > 0:
                print (f"\nAlready exists: {already_exists}")
                uptaded_moves[key] = already_exists
                continue
            
            follow_route = self.follow_route(moves, key)
            print (f"\nFollow route: {follow_route}")
            view_adjacents_nodes = self.see_adjacent_nodes(follow_route, key)
            print (f"\nView adjacents nodes: {view_adjacents_nodes}")
            uptaded_moves[key] = view_adjacents_nodes
        
        return uptaded_moves
            
    def already_exists(self, moves, key):
        already_exists = []
        
        for move in moves[key]:
            if self.adjacency_matrix[key[0]][key[1]].color == 1:
                list_moves = [move[0], key, move[1], move[2]]
            elif self.adjacency_matrix[key[0]][key[1]].color == 2:
                list_moves = [move[0], move[1], key, move[2], move[3]]
            
            if all(self.exist_connection(list_moves[i][0], list_moves[i][1], list_moves[i + 1][0], list_moves[i + 1][1]) for i in range(len(list_moves) - 1)):
                already_exists.append(move)
                
        return already_exists
    
    def follow_route(self, moves, key):
        new_moves = []
        connections = self.adjacency_matrix[key[0]][key[1]].adjacency_list
        list_connections = []

        if len(connections) == 0:
            return moves[key].copy()
        
        for node in connections:
            list_connections.append((node.x, node.y))
            
        for sublist in moves[key]:
            if all(elem in sublist for elem in list_connections):
                new_moves.append(sublist)
        
        return new_moves
    
    def get_coords_nodes(self, node_, directions):
        nodes = []
        for dx, dy in directions:
            new_x, new_y = node_[0] + dx, node_[1] + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                nodes.append((new_x, new_y))
        return nodes
    
    def valid_possible_moves_by_connections(self, list_moves, node_adj, connections):
        new_list_moves = []
        for play in list_moves:
            if play not in connections and play != node_adj:
                new_list_moves.append(play)
        return new_list_moves
    
    def see_adjacent_nodes(self, moves, key):
        view_adjacents_nodes = moves.copy()
        color = self.adjacency_matrix[key[0]][key[1]].color
        adj = [
            (-1, 0),  # up
            (0, -1),  # left
            (0, 1),   # right
            (1, 0),   # down
        ]

        diagonals = [
            (-1, -1),  # Diagonal up left
            (-1, 1),   # Diagonal up right
            (1, -1),   # Diagonal down left
            (1, 1)     # Diagonal down right
        ]

        nodes_adj = self.get_coords_nodes(key, adj)

        if color == 1:
            nodes_adj.extend(self.get_coords_nodes(key, diagonals))

        for move in moves:
            move_copy = move.copy()
            for node_adj in nodes_adj:
                if node_adj in move_copy:
                    weight = self.adjacency_matrix[node_adj[0]][node_adj[1]].weight
                    if weight > 0:
                        connections_ = self.adjacency_matrix[node_adj[0]][node_adj[1]].adjacency_list
                        connections = [(node.x, node.y) for node in connections_]

                        list_moves = []

                        if color == 1:
                            list_moves = [move_copy[0], key, move_copy[1], move_copy[2]]
                        elif color == 2:
                            list_moves = [move_copy[0], move_copy[1], key, move_copy[2], move_copy[3]]

                        list_moves = self.valid_possible_moves_by_connections(list_moves, node_adj, connections)
                        adj_ = self.get_coords_nodes(node_adj, adj)

                        count = sum(1 for di in adj_ if di in list_moves)

                        count += weight

                        if count > 2:
                            try:
                                view_adjacents_nodes.remove(move)
                            except:
                                pass

        return view_adjacents_nodes