from board import ALL_UNITS, update_values

def only_choice(history, values):
    """
    Eliminate values using the Only Choice strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        set_board_value(function): a method for performing board mutations
            It should take params (values_dict, target_box, new_value)

    Returns:
        The values dictionary with the naked twins eliminated from peers.
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