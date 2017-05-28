from board import BOXES, PEERS_OF, UNITS_OF, update_values

def naked_twins(history, values):
    """
    Eliminate values using the Naked Twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        set_board_value(function): a method for performing board mutations
            It should take params (values_dict, target_box, new_value)

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
        [box_1, box_2]
        for box_1 in candidate_twins
        for box_2 in PEERS_OF[box_1]
        if values[box_2] == values[box_1]
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