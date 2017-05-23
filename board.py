"""
This module sets utilities useful for working with the game board.
"""

def cross(a, b):
    """
    Cross product of elements in a and elements in b.
    """
    return [s+t for s in a for t in b]

# Rows are labeled with capital letters
rows = 'ABCDEFGHI'

# Columns are labeled with numbers
cols = '123456789'

# A box is a string of the form 'A1' or 'C5'
# representing one box on the game board.
boxes = cross(rows, cols)

# Units are groups of 9 squares which must contain one and only one of each
# of the digits 1 through 9. They come in 4 flavors: row, column, square, and diagonal.
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[''.join(x) for x in list(zip(rows, cols))], [''.join(x) for x in list(zip(rows[::-1], cols))]]
unitlist = row_units + column_units + square_units + diagonal_units

# This dict maps from boxes -> lists of all the units to which a box belongs.
units_of_box = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# The 'peers' of a given box are all the other boxes in the given box's units.
# If a box has a known value, none of its peers may take the same value.

# This dict maps from boxes -> peers of that box.
peers_of_box = dict((s, set(sum(units_of_box[s],[]))-set([s])) for s in boxes)