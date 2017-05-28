import board
from utils import get_strategies, convert_grid_string_to_dict, display

"""
This is a version of solution.py, which can't solve the AIND assignment,
as it relies on extenral modules and a 'strategies' package. It implements 
dynamic loading of strategies from the 'strategies' package. Any new
constraint prop strategy added in './strategies/' will automatically be
used in the solution.
"""

# A history of the 'moves' made in solving the sudoku.
# By 'move' we mean an assignment of a definite value to a box.
assignments = []

# A list of all strategies available in the strategies module
KNOWN_STRATEGIES = get_strategies()

def get_num_solved_boxes(values, num_options=0):
    return len([
        box 
        for box in values.keys() 
        if len(values[box]) == num_options
    ])

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
            values = strategy(assignments, values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = get_num_solved_boxes(values)

        # If no new values were added, stop the loop.
        has_stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        num_unsolvable_boxes = get_num_solved_boxes(values, 0)
        if num_unsolvable_boxes:
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
    if all(len(values[s]) == 1 for s in board.BOXES): 
        return values ## Solved!
                      ## 
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min(
        (len(values[s]), s) 
        for s in board.BOXES 
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

    return solved_game

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
