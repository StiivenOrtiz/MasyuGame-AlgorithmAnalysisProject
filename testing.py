class MayusGame:
    def __init__(self, pearls, size):
        self.pearls = pearls
        self.size = size
    
    def get_classify_pearls(self):
        white_pearls = []
        black_pearls = []
        
        for pearl in self.pearls:
            print(pearl.color)
            print(pearl.x)
            print(pearl.y)
            if pearl.color == 1:
                white_pearls.append(pearl)
            elif pearl.color == 2:
                print("black")
                black_pearls.append(pearl)
        return white_pearls, black_pearls
    
    def get_possible_black_pearl_moves(self, pearl):
        moves = []
        row, col = pearl.x, pearl.y
        size = self.size
        
        print(row, col)

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
                if self.adjacency_matrix[move[0][0]][move[0][1]].color == 2:
                    continue
                moves.append(move)

        return moves
    
    def solve_mayus_game(self):
        white_pearls, black_pearls = self.get_classify_pearls()
        first_black_pearl = black_pearls[0]
        return self.get_possible_black_pearl_moves(first_black_pearl)

# Definición de la perla para utilizarla en la clase
class Pearl:
    def __init__(self, row, col, color):
        self.x = row
        self.y = col
        self.color = color

# Ejemplo de uso
pearls = [Pearl((1 - 1), (3 - 1), 2),
          Pearl((1 - 1), (4 - 1), 2)]  # Solo una perla negra en (0, 0)
game = MayusGame(pearls, 5)  # Tablero de 5x5
jugadas = game.solve_mayus_game()
for jugada in jugadas:
    print(jugada)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def get_black_draw_connection(origin, play):
    connection_list = []
    for i in range(len(play) - 1):
        if play[i] == (origin[0], origin[1] + 1) or \
           play[i] == (origin[0], origin[1] - 1) or \
           play[i] == (origin[0] + 1, origin[1]) or \
           play[i] == (origin[0] - 1, origin[1]):
            connection_list.extend([origin, play[i], play[i], play[i + 1]])
    return connection_list


# Ejemplo de uso
origin = (0, 1)
play = [(0, 2), (0, 3), (1, 1), (2, 1)]
print(get_black_draw_connection(origin, play))

print(play)
















def get_white_draw_connection(origin, play):
    connection_list = []
    if play[0] == (origin[0], origin[1] + 1):
        connection_list.extend([play[0], origin, origin, play[1], play[1], play[2]])
    elif play[0] == (origin[0], origin[1] - 1):
        connection_list.extend([play[0], origin, origin, play[1], play[1], play[2]])
    elif play[0] == (origin[0] + 1, origin[1]):
        connection_list.extend([play[0], origin, origin, play[1], play[1], play[2]])
    elif play[0] == (origin[0] - 1, origin[1]):
        connection_list.extend([play[0], origin, origin, play[1], play[1], play[2]])
    
    return connection_list            
        
origin = (1, 2)
play = [(1, 1), (1, 3), (2, 3)]

print(get_white_draw_connection(origin, play))


def add_white_pearl_connections(self, lista: list[tuple]) -> None:
    """Add connections to the white pearls
    Args:
        lista (list[tuple]): The list of white pearls
    """
    for i in range(len(lista)):
        s_x, s_y = lista[i]
        e_x, e_y = lista[i + 1]
        if (0 <= e_x < self.size and 0 <= e_y < self.size):
            start_node = self.adjacency_matrix[s_x][s_y]
            end_node = self.adjacency_matrix[e_x][e_y]
            if end_node not in start_node.adjacency_list:
                # add weight
                end_node.weight += 1
                start_node.weight += 1
                # add node in the start node adjacent lis
                #t
                start_node.add_adjacent_node(end_node)
                
def clean_white_pearl_list(self, lista: list[tuple]) -> None:
        """Remove connections to the white pearls that already have two connections

        Args:
            lista (list[tuple]): The list of white pearls
        """
        for i in range(0, len(lista), 2):
            s_x, s_y = lista[i][0], lista[i][1]
            e_x, e_y = lista[i + 1][0], lista[i + 1][1]
            
            start_node = self.adjacency_matrix[s_x][s_y]
            end_node = self.adjacency_matrix[e_x][e_y]
            
            if end_node in start_node.adjacency_list or start_node in end_node.adjacency_list:
                lista.pop(i)
                lista.pop(i + 1)