import board

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    
    # All undecided boxes with exactly two possible value open
    candidate_twins = [
        box 
        for box in board.BOXES 
        if len(values[box]) == 2
    ]

    # If candidate_twin has a peer with identical value, these are naked_twins
    naked_twins_ = [
        [box_1, box_2]
        for box_1 in candidate_twins
        for box_2 in board.PEERS_OF[box_1]
        if values[box_2] == values[box_1]
    ]

    # Eliminate values from the naked twins' peers
    # 
    # This isn't quite right, we need to eliminate only within the correct unit,
    # not across all peers
    for (twin_1, twin_2) in naked_twins_:
        # determine the unit to which these twins both belong
        common_units = [
            unit 
            for unit in board.UNITS_OF[twin_1] 
            if twin_2 in unit
        ]
        
        for unit in common_units:
            for box in unit:
                for digit in values[twin_1]:
                    if box != twin_1 and box != twin_2:
                        values[box] = values[box].replace(digit, '')

    return values


def grid_values(grid):
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
    return dict(zip(board.BOXES, grid))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in board.BOXES)
    line = '  | ' + '+'.join(['-' * (width * 3)] * 3)
    print('    ' + ''.join(col.center(width) + ('|' if col in '36' else '') for col in board.COLS))
    print(line)
    for row in board.ROWS:
        print(row + ' | ' + ''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in board.COLS))
        if row in 'CF':
            print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    
    for box in solved_values:
        digit = values[box]
        for peer in board.PEERS_OF[box]:
            values[peer] = values[peer].replace(digit, '')
            
    return values

def only_choice(values):
    for unit in board.ALL_UNITS:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
            
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)


        # Your code here: Use the Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in board.BOXES): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in board.BOXES if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus
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

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
