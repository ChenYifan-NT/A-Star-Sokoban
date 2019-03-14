from sokoban import SokobanState

def problems_in():
    PROBLEMS = []

    file = open('Microban100.txt')

    row = 0
    col = 0

    player = []
    boxes = {} # boxes and targets are dictionaries so that the program can deal with problems that
    targets = {} # have restrictions on which box should go which storage. It is not used in the final test suite though.
    walls = []

    while True:

        line = file.readline()

        if not line:
            break
        if line.count('\n') == len(line): # skip blank rows
            continue
        if '#' not in line:
            player = tuple(player)
            walls = frozenset(tuple(walls))
            PROBLEMS.append(SokobanState(player, boxes, targets, walls, "start", None, 0))

            row = 0
            col = 0
            player = []
            boxes = {}
            targets = {}
            walls = []

        for char in line:
            if char == '#': # a wall
                walls.append((row, col))
            elif char == '@': #player
                player = [row, col]
            elif char == '$':
                boxes[(row, col)] = 0
            elif char == '.':
                targets[(row, col)] = 0
            elif char == '*':
                boxes[(row, col)] = 0
                targets[(row, col)] = 0
            elif char == '+':
                player = [row, col]
                targets[(row, col)] = 0
            col += 1

        col = 0
        row += 1

    return PROBLEMS