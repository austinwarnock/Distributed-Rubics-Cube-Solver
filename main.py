import json
import os.path

from cube import Cube
from solver import IDA_star, build_heuristic_db

MAX_MOVES = 7
NEW_HEURISTICS = False
HEURISTIC_FILE = 'heuristic.json'

cube = Cube()
print(cube)
print("-"*50)

if os.path.isfile(HEURISTIC_FILE):
    with open(HEURISTIC_FILE, 'r') as f:
        heuristic = json.load(f)
else:
    heuristic = None
    
if NEW_HEURISTICS or heuristic is None:
    actions = [(face, direction) for face in ['U', 'L', 'F', 'R', 'B', 'D'] for direction in ['clockwise', 'counterclockwise']]
    heuristic = build_heuristic_db(cube.stringify(), actions, MAX_MOVES, heuristic)
    
    with open(HEURISTIC_FILE, 'w', encoding='utf-8') as f:
        json.dump(heuristic, f, ensure_ascii=False, indent=4)
        
        
cube.scramble()
print(cube)

solver = IDA_star(heuristic, MAX_MOVES)
moves = solver.run(cube.stringify())
print(moves)

for move in moves:
    cube.rotate(move[0], move[1])
print(cube)
    