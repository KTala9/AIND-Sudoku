"""
A program for solving Diagonal Sudoku puzzles using search interwoven with 
constraint propagation (CP) strategies.

Currently three CP strategies are implemented, but more can be added by implementing 
a method for the strategy and adding it to the `KNOWN_STRATAGIES` list.
"""


# ==== UTILITIES ======================================================================

def cross(a, b):
    """
    Cross product of elements in a and elements in b.
    """
    return [
        s + t 
        for s in a 
        for t in b
    ]

def update_values(history, values, box, value):
    """
    Given a board state `values` and a move `box`, `values`, returns a new board
    state after that move has been made. Also saves this new board state to the
    `history` list.

    Args:
        history(list): A list of dicts, representing the game state for sequential moves
        values(dict): The dict storing the game state
        box(string): The key of the box to update e.g. 'A2'
        value(string): The new value for the given box e.g. '1' or '124789'
    Returns:
        A copy of the game state after the update is performed.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    new_values = values.copy()
    new_values[box] = value

    if len(value) == 1:
        history.append(new_values)

    return new_values

def convert_grid_string_to_dict(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.

    Args:
        grid(string) - A grid in string form.

    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"

    grid_list = [
        x if x != '.' else '123456789' 
        for x in grid
    ]

    return dict(zip(BOXES, grid_list))

def display(values):
    """
    Display the values as a 2-D grid.
    
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '  | ' + '+'.join(['-' * (width * 3)] * 3)
    print('    ' + ''.join(col.center(width) + ('|' if col in '36' else '') for col in COLS))
    print(line)
    for row in ROWS:
        print(row + ' | ' + ''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in COLS))
        if row in 'CF':
            print(line)
    return

def get_num_solved_boxes(values):
    """
    How many boxes are solved, in the sense that they have precisely one
    possible value?

    Returns:
        The number of solved boxes
    """
    return len([
        box 
        for box in values.keys() 
        if len(values[box]) == 1
    ])

def get_num_failed_boxes(values):
    """
    How many boxes have no possible values left?

    Returns:
        The number of failed/invalid/inconsistent boxes
    """
    return len([
        box 
        for box in values.keys() 
        if len(values[box]) == 0
    ])


# ==== BOARD CONSTANTS ======================================================================

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

ALL_UNITS = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAGONAL_UNITS

# This dict maps from boxes -> lists of all the units to which a box belongs.
UNITS_OF = dict((s, [u for u in ALL_UNITS if s in u]) for s in BOXES)

# The 'peers' of a given box are all the other boxes in the given box's units.
# If a box has a known value, none of its peers may take the same value.

# This dict maps from boxes -> peers of that box.
PEERS_OF = dict((s, set(sum(UNITS_OF[s], [])) - set([s])) for s in BOXES)


# ==== STRATAGIES ======================================================================

def elimination(values, history=[]):
    """
    Eliminate values using the Elimination strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        history(list): A list of previous game states (previous `values`)

    Returns:
        The values dictionary with inconsistent possibilities eliminated
        form all units.
    """
    solved_values = [
        box 
        for box in values.keys() 
        if len(values[box]) == 1
    ]
    
    for box in solved_values:
        digit = values[box]
        for peer in PEERS_OF[box]:
            new_value = values[peer].replace(digit, '')
            values = update_values(history, values, peer, new_value)

    return values

def only_choice(values, history=[]):
    """
    Eliminate values using the Only Choice strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        history(list): A list of previous game states (previous `values`)

    Returns:
        The values dictionary with any only-choice candidates set as decided box values.
    """
    for unit in ALL_UNITS:
        for digit in '123456789':

            dplaces = [
                box 
                for box in unit 
                if digit in values[box]
            ]

            if len(dplaces) == 1:
                values = update_values(history, values, dplaces[0], digit)

    return values

def naked_twins(values, history=[]):
    """
    Eliminate values using the Naked Twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        history(list): A list of previous game states (previous `values`)

    Returns:
        The values dictionary with the naked twins eliminated from peers.
    """
    
    # All undecided boxes with precisely two possible values
    candidate_twins = [
        box 
        for box in BOXES 
        if len(values[box]) == 2
    ]

    # If a candidate_twin has a peer with identical value, these are naked_twins
    # Trailing underscore is to avoid shadowing the method name.
    naked_twins_ = [
        (box_1, box_2)
        # They must have exactly two possible values
        for box_1 in candidate_twins
        # They must be peers
        for box_2 in PEERS_OF[box_1]
        # They must have the same two options
        if values[box_2] == values[box_1]
        # Don't double count
        if box_1 > box_2
    ]

    for (twin_1, twin_2) in naked_twins_:
        # Determine the units to which these twins both belong
        common_units = [
            unit 
            for unit in UNITS_OF[twin_1] 
            if twin_2 in unit
        ]
        
        # Eliminate the naked twins values from all their peers in these boxes
        for unit in common_units:
            for box in unit:
                for digit in values[twin_1]:
                    if box != twin_1 and box != twin_2:
                        new_value = values[box].replace(digit, '')
                        values = update_values(history, values, box, new_value)

    return values

"""
A list of all the constraint propagation strategies that though be used while
searching for a solution.
"""
KNOWN_STRATEGIES = [
    elimination, 
    only_choice, 
    naked_twins,
]

# ==== CORE PROGRAM ======================================================================

# A history of the 'moves' made in solving the sudoku.
# By 'move' we mean an assignment of a definite value to a box.
assignments = []

def reduce_puzzle(values):
    """
    Repeatedly apply every known strategy until there
    is no improvement of the board state

    Args:
        values(dict): The dict storing the game state

    Returns:
        The new game state.
    """
    has_stalled = False

    while not has_stalled:
        # Check how many boxes have a determined value
        solved_values_before = get_num_solved_boxes(values)

        # Apply every strategy the game knows
        for strategy in KNOWN_STRATEGIES:
            values = strategy(values, assignments)

        # Check how many boxes have a determined value, to compare
        solved_values_after = get_num_solved_boxes(values)

        # If no new values were added, stop the loop.
        has_stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        num_failed_boxes = get_num_failed_boxes(values)
        if num_failed_boxes:
            return False

    return values

def search(values):
    """
    Try to solve the Sudoku by repeatedly guessing values
    and applying constraint propagation.

    Args:
        values(dict): The dict storing the game state

    Returns:
        The new game state.
    """
    values = reduce_puzzle(values)

    if values is False:
        return False ## Failed earlier
                     ## 
    if all(len(values[s]) == 1 for s in BOXES): 
        return values ## Solved!
                      ## 
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min(
        (len(values[s]), s) 
        for s in BOXES 
        if len(values[s]) > 1
    )

    # Now use recurrence to solve each one of the resulting Sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.

    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = convert_grid_string_to_dict(grid)
    solved_game = search(values)

    if solved_game:
        return solved_game
    else:
        return false

if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')