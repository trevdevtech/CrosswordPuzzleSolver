import sys
import queue
import copy
import collections
import time

# word class is used to give a priority to 
# more common words for greedy heuristic
class Word:

	def __init__(self, word):
		self.word = word
		self.score = self.get_score(word)

	# increase word score based on letters found
	def get_score(self, word):
		score = 0.0;
		for char in self.word:
			if char == 'e':
				score += 11.16
			elif char == 'r':
				score += 7.5
			elif char == 't':
				score += 7.0
			elif char == 'n':
				score += 6.65
			elif char == 's':
				score += 5.7
			elif char == 'l':
				score += 5.4
		return score

	# used during sort of words
	def __lt__(self, other):
		return (self.score < other.score)

	# general output of a word object
	def __str__(self):
		return (self.word + " at " + str(self.score))

# The variable class is used represent a possible option for a word
# on the puzzle. Each slot in which a word may goes is a variable.
# Class houses all data needed by each variable
class Variable:

	def __init__(self, cell, direction, cell_pos, var_length, domain):
		self.cell = cell
		self.direction = direction
		self.pos = cell_pos
		self.length = var_length
		self.xrange = [0, 0]
		self.yrange = [0, 0]
		self.compute_xrange()
		self.compute_yrange()
		self.domain = domain # might need to be a deep copy
		self.choice = domain[0]
		self.cdomain = copy.deepcopy(self.domain)
		self.constraints = {}
		self.reverted = False
		self.start_c_letters = None
		self.start_c_positions = None

	# compute x bounds for a variable
	def compute_xrange(self):
		if self.direction == "across":
			self.xrange = [self.pos[0], self.pos[0] + (self.length - 1)]
		else:
			self.xrange = [self.pos[0], self.pos[0]]

	# compute y bounds for a word
	def compute_yrange(self):
		if self.direction == "down":
			self.yrange = [self.pos[1], self.pos[1] + (self.length - 1)]
		else:
			self.yrange = [self.pos[1], self.pos[1]]

	# check to see if a word overlaps with another
	def overlaps(self, other):
		xrangemet = False;
		yrangemet = False;
		if self.direction == "across":
			if self.xrange[0] <= other.pos[0] and other.pos[0] <= self.xrange[1]:
				xrangemet = True
			if other.yrange[0] <= self.pos[1] and self.pos[1] <= other.yrange[1]:
				yrangemet = True
		else:
			if other.xrange[0] <= self.pos[0] and self.pos[0] <= other.xrange[1]:
				xrangemet = True
			if self.yrange[0] <= other.pos[1] and other.pos[1] <= self.yrange[1]:
				yrangemet = True
			
		return (xrangemet and yrangemet)

	# gets the overlap coordinate if two variables overlap
	def get_overlap_pos(self, other):
		if not(self.overlaps(other)):
			return None;
		pos = []
		if self.direction == "across":
			pos.append(0)
			pos.append(other.pos[0])
			pos.append(self.pos[1])
		else:
			pos.append(1)
			pos.append(self.pos[0])
			pos.append(other.pos[1])
		return pos

	# used for sorting variables based on their constrained
	# domain sizes
	def __lt__(self, other):
		return (len(self.cdomain) < len(other.cdomain))
		
	# general output for variable object
	def __str__(self):
		if not(self.choice == None):
			return str(self.cell) + self.direction + " " + self.choice + "\n"
		cell = "cell: " + str(self.cell)
		direction = " direction: " + self.direction
		return (cell + direction + " domain: " + str(self.cdomain))

	# choosing a value for a variable and removing it from the
	# variables constrained domain
	def select(self):
		self.choice = self.cdomain.pop(0) # assume cdomain sorted

	# adding constraints to the variables
	def add_constraints(self, letters, positions):
		if (len(letters) != len(positions)):
			perror("Letters not match positions")
			exit(-1)
		for i in range(len(letters)):
			self.constraints[positions[i]] = letters[i]

	# removing all constaints for a variable except the
	# starting constraints
	def pop_all_constraints(self):
		self.constraints.clear()
		if not(self.start_c_letters == None) and not(self.start_c_positions == None):
			self.add_constraints(self.start_c_letters, self.start_c_positions)

	# constraining the domain based on the the variable's
	# constraints
	def constrain_domain(self):
		if self.reverted:
			return
		self.cdomain = []
		for word in self.domain:
			met_constraints = True
			for key in self.constraints:
				if key < len(word):
					if not(self.constraints[key] == word[key]):
						met_constraints = False
			if met_constraints:
				self.cdomain.append(word)

# function uses to stacks to solve the puzzle
# constrain domains of the variables, and populate the
# solution stack which is returned at the end
def solve_puzzle(vars_stack):

	solution_stack = []
	while len(vars_stack) > 0:

		# applying MRV sort
		vars_stack.sort(reverse = True)
		current_var = vars_stack.pop()

		# checking to see if backtrack required
		if len(current_var.cdomain) <= 0:
			current_var.reverted = False
			vars_stack.append(current_var)
			current_var.pop_all_constraints()

			if len(solution_stack) > 0:
				reverted = solution_stack.pop()
				reverted.reverted = True
				vars_stack.append(reverted)
		else:
			current_var.select()
			current_var.reverted = False
			solution_stack.append(current_var)

		# updating the contraints for all variables, based on the current solution set
		
		for current in vars_stack:
			current.pop_all_constraints()
			if current.reverted:
				continue
			for i, item in enumerate(solution_stack):
				if item.overlaps(current):
					overlap_pos = item.get_overlap_pos(current)
					if overlap_pos[0] == 0: # case item is across
						choice_index = overlap_pos[1] - item.pos[0]
						constraint_pos = overlap_pos[2] - current.pos[1]
						current.add_constraints([item.choice[choice_index]], [constraint_pos])
					else: # case item is down
						choice_index = overlap_pos[2] - item.pos[1]
						constraint_pos = overlap_pos[1] - current.pos[0]
						current.add_constraints([item.choice[choice_index]], [constraint_pos])

			current.constrain_domain()

	return solution_stack

def read_input(fn):
	fo = open(fn, 'r')
	lines = fo.readlines()
	puzzle = [[]] * len(lines)
	for i, line in enumerate(lines):
		puzzle[i] = list([char for char in line])
		puzzle[i].pop()
	return puzzle

# creates a dict of lists, where the key is the # of
# letters in a word and the value a sorted list of words
# words via the greedy heuristic
def build_domains(wordfile):
	fo = open(wordfile, 'r')
	lines = fo.readlines()
	words = {}
	for line in lines:
		line = line[:len(line)-1]
		if len(line) in words:
			words[len(line)].append(Word(line))
		else:
			words[len(line)] = [Word(line)]

	for key in words:
		words[key].sort()
	wrds = {}

	for key in words:
		for w in words[key]:
			if key in wrds:
				wrds[key].append(w.word)
			else:
				wrds[key] = [w.word]

	# remove high but uncommon word from set
	return wrds

