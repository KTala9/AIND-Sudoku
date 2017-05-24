import solution

"""
This module's purpose is simply to allow easy testing of the methods in the solution module.
"""

class Tester:
	board_initial = {
		'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
		'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
		'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
		'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
		'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
		'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
		'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
		'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
		'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
		'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
		'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'
	}

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