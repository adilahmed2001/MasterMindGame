from enum import Enum
import random
import time

MAX_ATTEMPTS = 20
NUMBER_OF_COLORS = 6

SEED_VALUE = 0

class GameStatus(Enum):
	WON = 1
	LOST = 0
	INPROGRESS = 2

class Colors(Enum):
	WHITE = 1 
	RED = 2
	GREEN = 3
	MAROON = 4
	PURPLE = 5
	YELLOW = 6
	BLUE = 7
	PINK = 8
	CYAN = 9
	ORANGE = 10
	GOLDEN = 11
	BROWN = 12

class Match(Enum):
	EXACT = 0
	NOTEXACT = 1
	NO = 2

globals().update(Match.__members__)
globals().update(GameStatus.__members__)
globals().update(Colors.__members__)

class AvailableColors(Enum):
	AVAILABLE_COLORS_POOL = [WHITE, RED, GREEN, MAROON, PURPLE, YELLOW, BLUE, PINK, CYAN, ORANGE]

globals().update(AvailableColors.__members__)

def check_selected_colors_are_unique(selected_colors): 
	if len(selected_colors) != len(set(selected_colors)): 
		raise Exception("Colors have to be distinct")

def check_number_of_provided_colors(provided_colors):
	if len(provided_colors) != NUMBER_OF_COLORS:
		raise Exception("Expecting 6 colors to be provided")

def check_number_of_selected_colors(selected_colors):
	if len(selected_colors) != NUMBER_OF_COLORS:
		raise Exception("Expecting 6 colors to be selected")

def guess(selected_colors, provided_colors):
	check_number_of_provided_colors(provided_colors)
	check_number_of_selected_colors(selected_colors)

	check_selected_colors_are_unique(selected_colors)

	match_for_position = lambda index: EXACT if selected_colors[index] == provided_colors[index] else\
    NOTEXACT if selected_colors[index] in provided_colors else NO

	return sorted( [match_for_position(index) for index in range(NUMBER_OF_COLORS)], key=lambda color: color.value)  

def check_max_attempts_not_exceeded(number_of_attempts):
	if number_of_attempts > MAX_ATTEMPTS:
		raise Exception("Game already completed, start a new Game")

def game_progress(number_of_attempts, is_winner):
	return WON if is_winner else LOST if number_of_attempts == MAX_ATTEMPTS else INPROGRESS

def is_winner(match_result):
	return (match_result == ([EXACT] * NUMBER_OF_COLORS))

def play(number_of_attempts, selected_colors, provided_colors):
	check_max_attempts_not_exceeded(number_of_attempts) 
	
	match_result = guess(selected_colors, provided_colors)

	return (game_progress(number_of_attempts, is_winner(match_result)), match_result)

def set_new_seed():
	global SEED_VALUE 
	SEED_VALUE = SEED_VALUE + 1

def select_distinct_colors():
	random.seed(SEED_VALUE)
	
	set_new_seed()

	return random.sample(AVAILABLE_COLORS_POOL.value, 6)