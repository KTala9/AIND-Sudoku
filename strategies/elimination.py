from board import PEERS_OF

def elimination(values, set_board_value):
    """
    Eliminate values using the Elimination strategy.
    WARNING: This method mutates `values`

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        The values dictionary with the naked twins eliminated from peers.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    
    for box in solved_values:
        digit = values[box]
        for peer in PEERS_OF[box]:
            new_value = values[peer].replace(digit, '')
            set_board_value(values, peer, new_value)
            
    return values