import sys
import queue
import copy
import collections
import time

from crossword_solver import Variable

def init_puzzle1():
	d1 = ["HOSES", "LASER", "SAILS", "SHEET", "STEER"]
	d4 = ["HEEL", "HIKE", "KEEL", "KNOT", "LINE"]
	d7 = ["AFT", "ALE", "EEL", "LEE", "TIE"]
	d8 = ["HOSES", "LASER", "SAILS", "SHEET", "STEER"]
	d2 = ["HOSES", "LASER", "SAILS", "SHEET", "STEER"]
	d3 = ["HOSES", "LASER", "SAILS", "SHEET", "STEER"]
	d5 = ["HEEL", "HIKE", "KEEL", "KNOT", "LINE"]
	d6 = ["AFT", "ALE", "EEL", "LEE", "TIE"]

	one = Variable(1, "across", [0, 0], 5, d1)
	two = Variable(2, "down", [2, 0], 5, d2)
	three = Variable(3, "down", [4, 0], 5, d3)
	four = Variable(4, "across", [1, 2], 4, d4)
	five = Variable(5, "down", [3, 2], 4, d5)
	six = Variable(6, "down", [0, 3], 3, d6)
	seven = Variable(7, "across", [2, 3], 3, d7)
	eight = Variable(8, "across", [0, 4], 5, d8)

	variables = [eight, seven, six, five, four, three, two, one]
	return variables

def init_puzzle2(word_dict):

	one = Variable(1, "across", [2,0], 7, word_dict[7])
	oned = Variable(1, "down", [2,0], 5, word_dict[5])
	two = Variable(2, "down", [8,0], 4, word_dict[4])
	three = Variable(3, "down", [11,1], 6, word_dict[6])
	four = Variable(4, "across", [5,3], 5, word_dict[5])
	five = Variable(5, "down", [7,3], 6, word_dict[6])
	six = Variable(6, "down", [4,5], 6, word_dict[6])
	seven = Variable(7, "across", [7,5], 5, word_dict[5])
	eight = Variable(8, "down", [9,5], 6, word_dict[6])
	nine = Variable(9, "down", [1,7], 4, word_dict[4])
	ten = Variable(10, "across", [3,7], 5, word_dict[5])
	eleven = Variable(11, "across", [0,9], 6, word_dict[6])

	variables = [eleven, ten, nine, eight, seven, six, five, four, three, two, oned, one]

	return variables

def init_puzzle3(word_dict):

	one = Variable(1, "across", [2, 0], 3, word_dict[3])
	oned = Variable(1, "down", [2,0], 8, word_dict[8])
	two = Variable(2, "down", [3,0], 3, word_dict[3])
	three = Variable(3, "down", [4,0], 4, word_dict[4])
	four = Variable(4, "across", [8,0], 3, word_dict[3])
	fourd = Variable(4, "down", [8,0], 4, word_dict[4])
	five = Variable(5, "down", [9,0], 3, word_dict[3])
	six = Variable(6, "down", [10, 0], 3, word_dict[3])
	seven = Variable(7, "across", [1,1], 5, word_dict[5])
	eight = Variable(8, "down", [5,1], 5, word_dict[5])
	nine = Variable(9, "across", [7,1], 5, word_dict[5])
	ten = Variable(10, "down", [11,1], 6, word_dict[6])
	eleven = Variable(11, "across", [1,2], 5, word_dict[5])
	elevend = Variable(11, "down", [1,2], 5, word_dict[5])
	twelve = Variable(12, "across", [7,2], 5, word_dict[5])
	twelved = Variable(12, "down", [7,2], 4, word_dict[4])
	thirteen = Variable(13, "across", [0,3], 3, word_dict[3])
	thirteend = Variable(13, "down", [0,3], 3, word_dict[3])
	fourteen = Variable(14, "across", [4,3], 5, word_dict[5])
	fifteen = Variable(15, "down", [6,3], 3, word_dict[3])
	sixteen = Variable(16, "across", [10,3], 3, word_dict[3])
	sixteend = Variable(16, "down", [10,3], 5, word_dict[5])
	seventeen = Variable(17, "down", [12,3], 3, word_dict[3])
	eighteen = Variable(18, "across", [0,4], 4, word_dict[4])
	nineteen = Variable(19, "down", [3,4], 5, word_dict[5])
	twenty = Variable(20, "across", [5,4], 3, word_dict[3])
	twenty1 = Variable(21, "across", [9,4], 4, word_dict[4])
	twenty2 = Variable(22, "across", [0,5], 4, word_dict[4])
	twenty3 = Variable(23, "across", [5,5], 3, word_dict[3])
	twenty4 = Variable(24, "across", [9,5], 4, word_dict[4])
	twenty4d = Variable(24, "down", [9,5], 4, word_dict[4])
	twenty5 = Variable(25, "across", [1,6], 4, word_dict[4])
	twenty6 = Variable(26, "down", [4,6], 4, word_dict[4])
	twenty7 = Variable(27, "across", [8,6], 4, word_dict[4])
	twenty7d = Variable(27, "down", [8,6], 4, word_dict[4])
	twenty8 = Variable(28, "across", [2,7], 4, word_dict[4])
	twenty9 = Variable(29, "down", [5,7], 4, word_dict[4])
	twenty9.start_c_letters = ['n']
	twenty9.start_c_positions = [3]
	twenty9.add_constraints(['n'], [3])
	twenty9.constrain_domain()
	thirty = Variable(30, "across", [7,7], 4, word_dict[4])
	thirtyd = Variable(30, "down", [7,7], 4, word_dict[4])
	thirtyd.start_c_letters = ['h']
	thirtyd.start_c_positions = [3]
	thirty.add_constraints(['h'],[3])
	thirty.constrain_domain()
	thirty1 = Variable(31, "across", [3,8], 7, word_dict[7])
	thirty2 = Variable(32, "down", [6,8], 4, word_dict[4])
	thirty2.start_c_letters = ['t']
	thirty2.start_c_postions = [2]
	thirty2.add_constraints(['t'], [2])
	thirty2.constrain_domain()
	thirty3 = Variable(33, "across", [4,9], 5, word_dict[5])

	variables = [one, oned, two, three, four, fourd, five, six, seven, eight, nine, ten, eleven, elevend, twelve, twelved, thirteen, thirteend, fourteen, fifteen, sixteen, sixteend, seventeen, eighteen, nineteen, twenty, twenty1, twenty2, twenty3, twenty4, twenty4d, twenty5, twenty6, twenty7, twenty7d, twenty8, twenty9, thirty, thirtyd, thirty1, thirty2, thirty3]
	return variables
