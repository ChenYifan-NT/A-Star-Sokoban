from astar import *

class SokobanState:

    index = 1

    def __init__(
        self, player, blocks, targets, walls,
        last_mov, predecessor, gval
    ):
        """
        @param player: tuple position of the player
        @param blocks: tuple positions of the blocks
        """

        self.player = player
        self.blocks = blocks
        self.targets = targets
        self.walls = walls
        self.last_mov = last_mov
        self.predecessor = predecessor
        self.gval = gval
        self.hval = hval_func(self)
        self.fval = fval_func(self)

    def successors(self):
        
        successors = []
        moving_cost = 1

        for mov in (UP, DOWN, LEFT, RIGHT):
            new_player_pos = mov.move(self.player)

            if new_player_pos in self.walls:
                continue
            
            if new_player_pos in self.blocks:
                new_box_pos = mov.move(new_player_pos)

                if new_box_pos in self.walls:
                    continue
                if new_box_pos in self.blocks:
                    continue
                if self.is_dead_block(new_box_pos):
                    continue

                new_boxes = dict(self.blocks)
                value = new_boxes.pop(new_player_pos)
                new_boxes[new_box_pos] = value
            else:
                new_boxes = self.blocks

            new_player = tuple(new_player_pos)

            new_sokoban_state = SokobanState(
                player=new_player, blocks=new_boxes, targets=self.targets, walls=self.walls,
                last_mov=mov.direction, predecessor=self,
                gval=self.gval + moving_cost
            )

            successors.append(new_sokoban_state)

        return successors

    def state_hash(self):
        """
        return the hash value of a sokoban state which is based on the positions of
        player and blocks.
        """
        return hash((self.player, frozenset(self.blocks.items())))

    def is_goal(self):
        """
        return True or False value on whether the state has reached the goal.
        """
        for box in self.blocks:
            if box not in self.targets:
                return False
        return True

    def has_loop(self):
        """
        return True or False value on whether the searching path has reached
        the same state before
        can avoid loop in the searching
        """
        prede = self.predecessor
        current_hash = self.state_hash()
        while prede:
            if prede.state_hash() == current_hash:
                return True
            prede = prede.predecessor
        return False

    def is_dead_block(self, moved_block_new_pos):
        """
        we want to check if a block is moved to a 'dead' position,
        where the block is surrounded by at least two adjacent walls,
        and the block is not on one of the targets.
        """

        if moved_block_new_pos in self.targets:
            return False

        for (trans_1, trans_2) in [
            (UP, LEFT), (UP, RIGHT),
            (DOWN, LEFT), (DOWN, RIGHT)
        ]:
            pos_1 = trans_1.move(moved_block_new_pos)
            pos_2 = trans_2.move(moved_block_new_pos)

            if pos_1 in self.walls and pos_2 in self.walls:
                return True

        return False

    def __lt__(self, other):
        """
        'less then' function used by headq
        """
        return self.fval < other.fval

    def print_board(self):
        height = max([wall[0] for wall in self.walls]) + 1
        width = max([wall[1] for wall in self.walls]) + 1

        board = []

        for i in range(height):
            row = []
            for j in range(width):
                row += [' ']
            board += [row]

        for storage in self.targets:
            board[storage[0]][storage[1]] = '+'
        for wall in self.walls:
            board[wall[0]][wall[1]] = '#'
        board[self.player[0]][self.player[1]] = 'x'
        for box in self.blocks:
            if box in self.targets:
                board[box[0]][box[1]] = '$'
            else:
                board[box[0]][box[1]] = '·'

        out = ''
        for row in board:
            for char in row:
                out += char
            out += '\n'

        print(out)


##################################################
class Movement():
    def __init__(self, direction, delta):
        """
        generize a new movement
        @param direction: the direction of movement
        @param delta: moving modification
        """
        self.direction = direction
        self.delta = delta

    def __hash__(self):
        return hash(self.direction)

    def __str__(self):
        return str(self.direction)

    def __repr__(self):
        return self.__str__()

    def move(self, position):
        return (position[0] + self.delta[0], position[1] + self.delta[1])

# coordinate starts from the upper left of the sokoban board
# global definitions on movements
# coordinate: (row, col)
UP = Movement('up', (-1, 0))
DOWN = Movement('down', (1, 0))
LEFT = Movement('left', (0, -1))
RIGHT = Movement('right', (0, 1))