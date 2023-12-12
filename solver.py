from cube import Cube
from random import choice
from tqdm import tqdm

class IDA_star():
    
    def __init__(self, heuristic, max_depth:int = 20):
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.threshold = max_depth
        self.min_threshold = None
        self.moves = []
        
    def run(self, state):
        while True:
            status = self.search(state, 1)
            if status: return self.moves
            self.moves = []
            self.threshold = self.min_threshold
            
    def check_threshold(self, cube:Cube, g):
        if cube.is_solved(): 
            return True
        elif g >= self.threshold: 
            return False
        else:
            return None
    def search(self, state, g):
        cube = Cube(state)
        
        
        current_threshold = self.check_threshold(cube, g)
        if current_threshold: 
            return current_threshold
        
        min_val = float('inf')
        best_action = []
        
        for face, direction in [(face, direction) for face in ['U', 'L', 'F', 'R', 'B', 'D'] for direction in ['clockwise', 'counterclockwise']]:
            cube = Cube(state)
            cube.rotate(face, direction)
            
            if cube.is_solved(): 
                self.moves.append((face, direction))
                return True
            
            cube_str = cube.stringify()
            h_score = self.heuristic[cube_str] if cube_str in self.heuristic else self.max_depth
            f_score = g + h_score
            
            if f_score < min_val:
                min_val = f_score
                best_action = [(cube_str,(face, direction))]
            elif f_score == min_val:
                best_action.append((cube_str,(face, direction)))
        
        if best_action is not None:
            if self.min_threshold is None or min_val < self.min_threshold:
                self.min_threshold = min_val
            next_action = choice(best_action)
            self.moves.append(next_action[1])
            status = self.search(next_action[0], g + 1)
            if status: return status
        return False


def build_heuristic_db(state, actions, max_moves = 20, heuristic = None):
    if heuristic is None:
        heuristic = {state: 0}
    queue = [(state, 0)]
    node_count = sum([len(actions) ** (x + 1) for x in range(max_moves + 1)])
    with tqdm(total=node_count, desc='Heuristic DB') as pbar:
        while True:
            if not queue:break
            
            s, d = queue.pop()
            if d > max_moves:continue
            
            for face, direction in actions:
                cube = Cube(state=s)
                cube.rotate(face, direction)
                a_str = cube.stringify()
                if a_str not in heuristic or heuristic[a_str] > d + 1:
                    heuristic[a_str] = d + 1
                queue.append((a_str, d+1))
                pbar.update(1)
    return heuristic
