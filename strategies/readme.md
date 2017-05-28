# Adding strategies

New strategies can be added to the Sudoku player
by adding strategy modules to this `strategies` package.

At a minimum a new strategy module should contain one method,
of the same name as the module. This method is expected to
take params `history(list), values(dict)`, and is responsible for updating
the board state (by mutating `values`) and updating the `history` by appending
