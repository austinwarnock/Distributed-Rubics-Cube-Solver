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
        self.squares = [[f"{color.value}{(r * 3) + c + 1}" for c in range(3)] for r in range(3)]
        
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
        if len(self.squares) != 3 or len(self.squares[0]) != 3:
            return "Input self.squares is not 3x3"

        top = self.squares[0]
        bottom = self.squares[2]
        left = [row[0] for row in self.squares]
        right = [row[2] for row in self.squares]

        if direction == "clockwise":
            self.set_row(0, left[::-1])
            self.set_column(2, top)
            self.set_row(2, right[::-1])
            self.set_column(0, bottom)
        elif direction == "counterclockwise":
            self.set_row(0, right)
            self.set_column(2, bottom[::-1])
            self.set_row(2, left)
            self.set_column(0, top[::-1])

        
    def get_row(self, row: int):
        return self.squares[row]
    
    def get_column(self, column: int):
        return [row[column] for row in self.squares]
        
    def get_row_for_print(self, row: int):
        return "|".join(s for s in self.squares[row])
        
        
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
          ('L', 'r',0),
          ('B', 'r',0),
          ('R', 'r',0)
          ],
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
          ('L', 'c',0),
          ('D', 'r',2), 
          ('R', 'c',2)
          ],
    'D': [('F','r',2), 
          ('R', 'r',2),
          ('B', 'r',2),
          ('L', 'r',2)]
}
    

class Cube:
    
    def __init__(self):
        self.faces = {
            'U': Face(Color.YELLOW),
            'L': Face(Color.BLUE),
            'F': Face(Color.RED),
            'R': Face(Color.GREEN),
            'B': Face(Color.ORANGE),
            'D': Face(Color.WHITE)
        }
        
    def get_values(self, face_arr:list, index_arr:list, type_arr:list):
        out = []
        for face, idx, type in zip(face_arr, index_arr, type_arr):
            if type == 'r':
                out.append(self.faces[face].get_row(idx))
            else:
                out.append(self.faces[face].get_column(idx))
        return self.shift_list(out)
    
    def set_values(self, face_arr:list, index_arr:list, type_arr:list, values:list):
        for face, idx, type, value in zip(face_arr, index_arr, type_arr, values):
            if type == 'r':
                self.faces[face].set_row(idx, value)
            else:
                self.faces[face].set_column(idx, value)
                
    def shift_list(self, lst:list):
        lst.insert(0, lst.pop())
        return lst
        
    def rotate_x(self, move:str, direction: str): #U,D
        type_lst = ['r','r','r','r']
        if move == 'U':
            faces = ['F','L','B','R']
            idx_lst = [0,0,0,0]
        else:
            faces = ['F','R','B','L']
            idx_lst = [2,2,2,2]
            
        if direction == 'counterclockwise':
            faces = faces[::-1]
            idx_lst = idx_lst[::-1]
            type_lst = type_lst[::-1]
            
        values = self.get_values(faces, idx_lst, type_lst)
        
        self.set_values(faces, idx_lst, type_lst, values)
    
        
    def rotate_y(self, move:str, direction: str): # L,R
        type_lst = ['c','c','c','c']
        flip_ids = [0,-1]
        
        if move == 'L': #B -> U, D-> B
            faces = ['U','F','D','B']
            idx_lst = [0,0,0,2]
        else: #U -> B, B-> D
            faces = ['D','F','U','B']
            idx_lst = [2,2,2,0]
            
        if direction == 'counterclockwise':
            faces = faces[::-1]
            idx_lst = idx_lst[::-1]
            type_lst = type_lst[::-1]
            flip_ids = [-1,0]
            
        values = self.get_values(faces, idx_lst, type_lst)
        values[flip_ids[0]] = values[0][::-1]
        values[flip_ids[1]] = values[-1][::-1]         
        self.set_values(faces, idx_lst, type_lst, values)
        
        
    def rotate_z(self, move:str, direction: str): # F,B
        type_lst = ['r','c','r','c']
        
        if move == 'F': #R -> D, L -> U
            type_lst = ['r','c','r','c']
            faces = ['U','R','D','L']
            idx_lst = [2,0,0,2]
        else: # D-R, U-L
            type_lst = ['c','r','c','r']
            faces = ['L','D','R','U']
            idx_lst = [0,2,2,0]
    
        values = self.get_values(faces, idx_lst, type_lst)
        values[0] = values[0][::-1]
        values[2] = values[2][::-1]
        
        
        self.set_values(faces, idx_lst, type_lst, values)


        
    def update_adjacent_faces(self, face: str, direction: str):
        if face not in self.faces.keys():
            raise ValueError("face must be one of 'U', 'L', 'F', 'R', 'B', 'D'")
        
        if face == 'U' or face == 'D':
            self.rotate_x(face, direction)
        elif face == 'L' or face == 'R':
            self.rotate_y(face, direction)
        elif face == 'F' or face == 'B':
            self.rotate_z(face, direction)
        

            
        

        
    def rotate(self, face: str, direction: str):
        if face not in self.faces.keys():
            raise ValueError("face must be one of 'U', 'L', 'F', 'R', 'B', 'D'")
        self.faces[face].rotate(direction)
        self.update_adjacent_faces(face, direction)

    def print_move(self, face: str, direction: str):
        print(f"{face}{'`' if direction == 'counterclockwise' else ''}")
        
    def scramble(self):
        from random import choice
        for _ in range(5):
            face = choice(list(self.faces.keys()))
            direction = choice(['clockwise', 'counterclockwise'])
            self.print_move(face, direction)
            self.rotate(face, direction)
            print(self.__str__())
        
    def __str__(self):
        # print the net of the cube
        out = ""
        for i in range(3):
            out += "         " + str(self.faces['U'].get_row_for_print(i)) + "\n"
        for i in range(3):
            out += str(self.faces['L'].get_row_for_print(i)) + "|"
            out += str(self.faces['F'].get_row_for_print(i)) + "|"
            out += str(self.faces['R'].get_row_for_print(i)) + "|"
            out += str(self.faces['B'].get_row_for_print(i)) + "\n"
        for i in range(3):
            out += "         " + str(self.faces['D'].get_row_for_print(i)) + "\n"
                

        return out


if __name__ == "__main__":
    c = Cube()
    print(c)
    
    for direction in ['clockwise', 'counterclockwise']:
        for face in ['U', 'L', 'F', 'R', 'B', 'D']:
            c = Cube()
            file = open(f"tests/{face}-{direction}.txt", "w")
            c.rotate(face, direction)
            print(c, file=file)


    #c.scramble()
    # c.rotate('U', 'counterclockwise')
    # print(c)
    # c.rotate('D', 'clockwise')
    # print(c)
    # c.rotate('B', 'clockwise')
    # print(c)
    # c.rotate('R', 'counterclockwise')

    print(c)

