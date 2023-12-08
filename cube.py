from enum import Enum

class Color(Enum):
    RED = 'R'
    GREEN = 'G'
    BLUE = 'B'
    YELLOW = 'Y'
    WHITE = 'W'
    ORANGE = 'O'

class Face:
    def __init__(self, color: Color):
        self.color = color
        self.squares = [[color for _ in range(3)] for __ in range(3)]
        
    def set_row(self, row: int, squares: list):
        if len(squares) != 3:
            raise ValueError("squares must be a list of length 3")
        self.squares[row] = squares
    
    def set_column(self, column: int, squares: list):
        if len(squares) != 3:
            raise ValueError("squares must be a list of length 3")
        for i in range(3):
            if type(self.squares[i]) != Color:
                self.squares[i] = list(self.squares[i])
            self.squares[i][column] = squares[i]
        
    def rotate(self, direction: str):
        if direction == "clockwise":
            self.squares = list(zip(*self.squares[::-1]))
        elif direction == "counterclockwise":
            self.squares = list(zip(*self.squares))[::-1]
        else:
            raise ValueError("direction must be either 'clockwise' or 'counterclockwise'")
        
    def get_row(self, row: int):
        return self.squares[row]
    
    def get_column(self, column: int):
        return [row[column] for row in self.squares]
        
    def get_row_for_print(self, row: int):
        return "|".join(s.value for s in self.squares[row])
        
        
    def __str__(self):
        out = ""
        for row in self.squares:
            out += "|"
            for square in row:
                out += square.value + "|"
            out += "\n"
        return out

    
EDGE_ADJACENCY = {
    'U': [('F','r',0), 
          ('R', 'r',0),
          ('B', 'r',0),
          ('L', 'r',0)],
    'L': [('U', 'c',0),
          ('F','c',0), 
          ('D', 'c',0),
          ('B', 'c',2)],
    'F': [('U','r',2), 
          ('R', 'c',0),
          ('D', 'r',0),
          ('L', 'c',2)],
    'R': [('F','c',2), 
          ('U', 'c',2),
          ('B', 'c',0),
          ('D', 'c',2)],
    'B': [('U','r',0), 
          ('R', 'c',2),
          ('D', 'r',2),
          ('L', 'c',0)],
    'D': [('F','r',2), 
          ('R', 'r',2),
          ('B', 'r',2),
          ('L', 'r',2)]
}
    

class Cube:
    
    def __init__(self):
        self.faces = {
            'U': Face(Color.WHITE),
            'L': Face(Color.GREEN),
            'F': Face(Color.RED),
            'R': Face(Color.BLUE),
            'B': Face(Color.ORANGE),
            'D': Face(Color.YELLOW)
        }
        
    def update_adjacent_faces(self, face: str, direction:str):
        lookup = EDGE_ADJACENCY[face]
        if direction == "counterclockwise":
            lookup = lookup[::-1]
        
        prev = []

        for lookup_index, (adj_face, mod_type, index) in enumerate(lookup):
            temp = []
            if lookup_index == 0:
                last_face = lookup[-1][0]
                last_type = lookup[-1][1]
                last_index = lookup[-1][2]
                prev = self.faces[last_face].get_row(last_index) if last_type == 'r' else self.faces[last_face].get_column(last_index)
            else:
                last_face = lookup[lookup_index-1][0]
                last_type = lookup[lookup_index-1][1]
                last_index = lookup[lookup_index-1][2]    
            
            temp = self.faces[adj_face].get_row(index) if mod_type == 'r' else self.faces[adj_face].get_column(index)
            self.faces[adj_face].set_row(index, prev) if mod_type == 'r' else self.faces[adj_face].set_column(index, prev)
            
            prev = temp

        
    def rotate(self, face: str, direction: str):
        if face not in self.faces.keys():
            raise ValueError("face must be one of 'U', 'L', 'F', 'R', 'B', 'D'")
        self.faces[face].rotate(direction)
        self.update_adjacent_faces(face, direction)
        
    def scramble(self):
        from random import choice
        for _ in range(100):
            face = choice(list(self.faces.keys()))
            direction = choice(['clockwise', 'counterclockwise'])
            self.rotate(face, direction)
        
    def __str__(self):
        # print the net of the cube
        out = ""
        for i in range(3):
            out += "      " + str(self.faces['U'].get_row_for_print(i)) + "\n"
        for i in range(3):
            out += str(self.faces['L'].get_row_for_print(i)) + "|"
            out += str(self.faces['F'].get_row_for_print(i)) + "|"
            out += str(self.faces['R'].get_row_for_print(i)) + "|"
            out += str(self.faces['B'].get_row_for_print(i)) + "\n"
        for i in range(3):
            out += "      " + str(self.faces['D'].get_row_for_print(i)) + "\n"
                

        return out


if __name__ == "__main__":
    c = Cube()
    print(c)
    
    c.scramble()

    print(c)

