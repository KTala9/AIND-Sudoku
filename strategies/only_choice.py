from board import ALL_UNITS

def only_choice(values, set_board_value):
    """
    Eliminate values using the Only Choice strategy.
    WARNING: This method mutates `values`

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with the naked twins eliminated from peers.
    """
    for unit in ALL_UNITS:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                set_board_value(values, dplaces[0], digit)
            
    return values