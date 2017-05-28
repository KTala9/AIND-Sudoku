from board import PEERS_OF, update_values

def elimination(history, values):
    """
    Eliminate values using the Elimination strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
		set_board_value(function): a method for performing board mutations
			It should take params (values_dict, target_box, new_value)

    Returns:
        The values dictionary with the naked twins eliminated from peers.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    
    for box in solved_values:
        digit = values[box]
        for peer in PEERS_OF[box]:
            new_value = values[peer].replace(digit, '')
            values = update_values(history, values, peer, new_value)

    return values