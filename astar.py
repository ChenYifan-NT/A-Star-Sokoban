# global settings on A* functions
import copy

HVAL_FUNC = ['trivial', 'manhattan_a', 'manhattan_b', 'along_the_wall']

HEUR = HVAL_FUNC[0]
def hval_func(state):
    ans = 0
    if HEUR == 'trivial':
        ans = heur_trivial(state)
    elif HEUR == 'manhattan_a':
        ans = heur_manhattan_distance_a(state)
    elif HEUR == 'manhattan_b':
        ans = heur_manhattan_distance_b(state)
    elif HEUR == 'along_the_wall':
        ans == heur_along_the_wall(state)

    return ans

def heur_trivial(state):
    count = 0
    for blk in state.blocks:
        if blk not in state.targets:
            count += 1
    return count   

def heur_manhattan_distance_a(state):
    min_dist = float('inf')
    manhattan_distance = 0
    for box in state.blocks:
        for storage in state.targets:
            cur_dist = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            if cur_dist < min_dist:
                min_dist = cur_dist
        manhattan_distance += min_dist
        min_dist = float('inf')
    return manhattan_distance

def heur_manhattan_distance_b(state):
    boxes = copy.deepcopy(state.blocks)
    storages = copy.deepcopy(state.targets)
    manhattan_distance = 0
    min_dist = float('inf')
    min_box = ()
    for storage in storages:
        for box in boxes:
            cur_dist = abs(storage[0] - box[0]) + abs(storage[1] - box[1])
            if cur_dist < min_dist:
                min_dist = cur_dist
                min_box = box
        manhattan_distance += min_dist
        if boxes:
            boxes.pop(min_box)
        min_dist = float('inf')

    return manhattan_distance

def heur_along_the_wall(state): # mostly we don't want our blocks to be alongside the wall
    punish_weight = 0.2
    # dead block is already checked in sokoban state, here we check if the block is alongside the wall
    # if it isn't, use manhattan distance as the heul
    # if there is a storage along the wall, pass
    # otherwise set the heul to be infinite

    h_man = heur_manhattan_distance_a(state)
    heur = h_man

    # check if the boxes are alongside the walls
    for box in state.blocks:
        row = box[0]
        col = box[1]

        # check vertically
        if (row, col - 1) in state.walls or (row, col + 1) in state.walls:
            # now we start to check the area around the box and give a punishment to the hval everytime we detect a wall
            # in case there is problem, use deep copy here
            up = copy.deepcopy(row)
            down = copy.deepcopy(row)
            cur_row = copy.deepcopy(row)
            while True:
                if (cur_row + 1, col) in state.targets: # there is a storage along the route, no punishment
                    return h_man
                elif (cur_row + 1, col) in state.walls:
                    break
                down += 1
                cur_row += 1
            cur_row = copy.deepcopy(row)
            while True:
                if (cur_row - 1, col) in state.targets: # there is a storage along the route, no punishment
                    return h_man
                elif (cur_row - 1, col) in state.walls:
                    break
                up += 1
                cur_row -= 1

            for r in range(up, down + 1):
                if (r, col - 1) in state.walls:
                    heur += punish_weight * h_man
                if (r, col + 1) in state.walls:
                    heur += punish_weight * h_man


        # check horizontally
        if (row - 1, col) in state.walls or (row + 1, col) in state.walls:
            # now we start to check the area around the box and give a punishment to the hval everytime we detect a wall
            left = copy.deepcopy(col)
            right = copy.deepcopy(col)
            cur_col = copy.deepcopy(col)
            while True:
                if (row, cur_col + 1) in state.targets: # there is a storage along the route, no punishment
                    return h_man
                elif (row, cur_col + 1) in state.walls:
                    break
                right += 1
                cur_col += 1
            cur_col = copy.deepcopy(col)
            while True:
                if (row, cur_col - 1) in state.targets: # there is a storage along the route, no punishment
                    return h_man
                elif (row, cur_col - 1) in state.walls:
                    break
                left += 1
                cur_col -= 1

            for c in range(left, right + 1):
                if (row - 1, c) in state.walls:
                    heur += punish_weight * h_man
                if (row + 1, c) in state.walls:
                    heur += punish_weight * h_man

    return heur

def fval_func(state):
    return state.gval + state.hval