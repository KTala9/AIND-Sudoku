"""
This module sets utilities useful for working with the game board.
"""

def cross(a, b):
    """
    Cross product of elements in a and elements in b.
    """
    return [s+t for s in a for t in b]

# Rows are labeled with capital letters
ROWS = 'ABCDEFGHI'

# Columns are labeled with numbers
COLS = '123456789'

# A box is a string of the form 'A1' or 'C5'
# representing one box on the game board.
BOXES = cross(ROWS, COLS)

# Units are groups of 9 squares which must contain one and only one of each
# of the digits 1 through 9. 
# 
# They come in 4 flavors: row, column, square, and diagonal.
ROW_UNITS = [cross(r, COLS) for r in ROWS]

COLUMN_UNITS = [cross(ROWS, c) for c in COLS]

SQUARE_UNITS = [
    cross(rs, cs) 
    for rs in ('ABC', 'DEF', 'GHI') 
    for cs in ('123', '456', '789')
]

DIAGONAL_UNITS = [
    [''.join(x) for x in list(zip(ROWS, COLS))], 
    [''.join(x) for x in list(zip(ROWS[::-1], COLS))]
]

ALL_UNITS = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS

ALL_UNITS_INC_DIAG = ROW_UNITS \
    + COLUMN_UNITS + SQUARE_UNITS + DIAGONAL_UNITS

# This dict maps from boxes -> lists of all the units to which a box belongs.
UNITS_OF = dict((s, [u for u in ALL_UNITS if s in u]) for s in BOXES)

# The 'peers' of a given box are all the other boxes in the given box's units.
# If a box has a known value, none of its peers may take the same value.

# This dict maps from boxes -> peers of that box.
PEERS_OF = dict((s, set(sum(UNITS_OF[s], [])) - set([s])) for s in BOXES)