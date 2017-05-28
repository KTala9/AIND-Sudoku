import solution

"""
This module's purpose is simply to allow easy testing of the methods in the solution module.
"""

grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'

board = solution.convert_grid_string_to_dict(grid)

class Tester:
	board_initial = board

	def test_solution(self):
		solution.display(self.board_initial)

		print('================= Try naked twins =================')

		game_copy_1 = self.board_initial.copy()

		naked_twins_sudoku = solution.naked_twins(game_copy_1)

		if naked_twins_sudoku:
			solution.display(naked_twins_sudoku)
		else:
			print('No solution found')

		print('================= Try reduction with multiple techniques =================')
		
		game_copy_2 = self.board_initial.copy()
		solved_sudoku = solution.search(game_copy_2)

		if solved_sudoku:
			solution.display(solved_sudoku)
		else:
			print('No solution found')

def main():
	tester = Tester()
	tester.test_solution()

if __name__ == '__main__':
	main()