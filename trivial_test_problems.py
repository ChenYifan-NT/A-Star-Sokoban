from sokoban import SokobanState
# problems are from http://www.4399.com/flash/9380_3.htm
# I used to play lots of flash games on 4399.com when I was a child
# These two problems are used to test the codes, and are not parts of the final testing suite

TEST_PROBLEMS = [
    SokobanState( # level 1
    (4, 3), # player
    {
        (1, 4): 0,
        (2, 4): 1,
        (4, 2): 2,
        (5, 2): 3}, # boxes
    {   
        (1, 2): 0,
        (1, 3): 1,
        (5, 1): 2,
        (6, 1): 3}, # targets
    frozenset((
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 0), (1, 6),
        (2, 0), (2, 2), (2, 6),
        (3, 0), (3, 2), (3, 4), (3, 6),
        (4, 0), (4, 4), (4, 6),
        (5, 0), (5, 6),
        (6, 0), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
        (7, 0), (7, 1), (7, 2)
    )), # walls
    "start", # last_mov
    None, # predesessor
    0 # gval
    ),

    SokobanState( # level 2 f1n3
    (4, 6), # player
    { # boxes
        (2, 6): 0,
        (3, 6): 1},
    { # targets
        (4, 2): 0,
        (4, 4): 1},
    frozenset( # walls
        (
            (0, 2), (0, 3), (0, 4), (0, 5),
            (1, 0), (1, 1), (1, 2), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 0), (2, 8),
            (3, 0), (3, 2), (3, 5), (3, 8),
            (4, 0), (4, 5), (4, 8),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)
        )),
        "start", # last_mov
        None, # predesessor
        0 # gval
    )
]