import pkgutil
from board import ROWS, COLS, BOXES

def get_strategies():
    """
    Gets a list of all available strategies

    Returns:
        A list of methods, each representing a strategy from the strategies module
    """
    strategy_names = [name for _, name, _ in pkgutil.iter_modules(['strategies'])]

    strategy_methods = []

    for strategy in strategy_names:
        module_name = "strategies." + strategy
        module = __import__(module_name, fromlist=[''])
        method = getattr(module, strategy)
        strategy_methods.append(method)

    return strategy_methods

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

    grid_list = [x if x != '.' else '123456789' for x in grid]

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