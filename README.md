# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: 
Sudoku puzzles involve the constraint that each value in range(1,9) may appear
in a unit once and only once. All constraint propagation strategies in sudoku rely
on this constraint. If it can be determined that a given digit must occur in some subset
of boxes in a unit, the constraint allows us to determine that that digit cannot occur
in any other box in that unit. Hence the constraint can be propagated to other boxes,
reducing the domain of possible values that box can take.

In the case of naked twins, the subset of a unit we are looking for is one with exactly
two boxes which share the same two possible digit values. In such subsets, one box must 
take one value, and the other box the other value. Regardless of how the digits are assigned,
the remaining boxes in the given unit cannot take either of those digits as their value.

By identifying naked twins in each unit, and applying the above reasoning, we eliminate
possible values of the remaining squares, and essentially prune the search tree we need
to explore to solve the sudoko, bringing us closer to a complete solution.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: 
To solve the diagonal sudoku problem, we first preprocess the board by applying
three constraint propagation strategies: elimination, only-choice, and naked-twins.
Each of these works by applying sudoku's main constraint: that the digits in range(1,9)
must each appear only once in a unit. The general pattern is that, for a given unit, 
we identify a subset of n boxes for which there are only n remaining possible values. 
These values can then be removed as possibilities from the other boxes in the given unit.
This reduces the size of the remaining search problem.

Once the constraint propagation strategies yield no further change in the sudoku's state,
we search, basically guessing a value. At each step int he search we apply out constraint
propagation strategies again, either reducing the problem, or leading to an inconsistent state
(in which case we must backtrack). By using CP at each step, we can greatly reduce the size of
the search tree. Proceeding in this fashion will yield either a solution, or only inconsistent
states (in which case the sudoku is unsolvable).


### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

