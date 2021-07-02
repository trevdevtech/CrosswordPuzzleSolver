import sys
import queue
import copy
import collections
import time

from crossword_solver_inputs import init_puzzle1
from crossword_solver_inputs import init_puzzle2
from crossword_solver_inputs import init_puzzle3

from crossword_solver import build_domains
from crossword_solver import solve_puzzle

def main():

	if len(sys.argv) < 2:
		print("error, need to specify word bank")
		exit(-1)

	if len(sys.argv) < 3:
		print("error, need to choose a puzzle, type 1, 2 or 3")
		print("defaulting to puzzle 3:")

	puzzle_number = sys.argv[2]

	domains = build_domains(sys.argv[1])

	if puzzle_number == '1':
		variables = init_puzzle1()
	elif puzzle_number == '2':
		variables = init_puzzle2(domains)
	elif puzzle_number == '3':
		variables = init_puzzle3(domains)

	init_time = time.time()
	print('\033[96m' + "Solving Puzzle:" + '\033[0m')
	solution = solve_puzzle(variables)

	print('\033[92m' + "SOLUTION in " + (str(time.time() - init_time)) + '\033[0m')
	print("Solution size: " + str(len(solution)))
	print(*solution)

main()
