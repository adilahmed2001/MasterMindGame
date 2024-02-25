import unittest
from enum import Enum
from src.mastermind import *
from parameterized import parameterized

class MasterMindTests(unittest.TestCase):

	def test_canary(self):
		self.assertTrue(True)

	@parameterized.expand([
		( [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [EXACT, EXACT, EXACT, EXACT, EXACT, EXACT]),
		( [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ BLUE, PINK, CYAN, ORANGE, GOLDEN, BROWN], [NO, NO, NO, NO, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ RED, WHITE, MAROON, GREEN, YELLOW, PURPLE], [NOTEXACT, NOTEXACT, NOTEXACT, NOTEXACT, NOTEXACT, NOTEXACT]),
		( [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, GOLDEN, BROWN], [EXACT, EXACT, EXACT, EXACT, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ GOLDEN, BROWN, GREEN, MAROON, PURPLE, YELLOW], [EXACT, EXACT, EXACT, EXACT, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, YELLOW, PURPLE], [ WHITE, RED, GREEN, YELLOW, PURPLE, MAROON], [EXACT, EXACT, EXACT, NOTEXACT, NOTEXACT, NOTEXACT]),
		( [ WHITE, RED, GREEN, MAROON, YELLOW, PURPLE], [ GOLDEN, RED, BROWN, YELLOW, PURPLE, MAROON], [EXACT, NOTEXACT, NOTEXACT, NOTEXACT, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, YELLOW, PURPLE], [ WHITE, WHITE, WHITE, WHITE, WHITE, WHITE], [EXACT, NO, NO, NO, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, YELLOW, PURPLE], [ PURPLE, PURPLE, PURPLE, PURPLE, PURPLE, PURPLE], [EXACT, NO, NO, NO, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, YELLOW, PURPLE], [ RED, WHITE, WHITE, WHITE, WHITE, WHITE], [NOTEXACT, NOTEXACT, NO, NO, NO, NO]),
		( [ WHITE, RED, GREEN, MAROON, YELLOW, PURPLE], [ GOLDEN, WHITE, WHITE, WHITE, WHITE, WHITE], [NOTEXACT, NO, NO, NO, NO, NO])
	])
	def test_guessParameterized(self, selected_colors, provided_colors, expected_result):
                
		self.assertEqual(guess(selected_colors, provided_colors), expected_result)


	def test_guessWithRepeatSelectedColors(self):    	
		selected_colors = [ WHITE, PINK, CYAN, ORANGE, GOLDEN, WHITE]
    
		with self.assertRaises(Exception) as context:			
			guess(selected_colors, [WHITE, RED, GREEN, MAROON, YELLOW, PURPLE])
		
		self.assertEqual(str(context.exception), "Colors have to be distinct")


	@parameterized.expand([
		( [ RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW]),
		( [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE])
	])		
	def test_guesswithColorsNotEqualToSix(self, selected_colors, provided_colors):
		
		with self.assertRaises(Exception) as context:		
			guess(selected_colors, provided_colors)

		self.assertTrue( str(context.exception) in ["Expecting 6 colors to be provided","Expecting 6 colors to be selected"] )


	@parameterized.expand([
		( 1, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], (WON, [ EXACT, EXACT, EXACT, EXACT, EXACT, EXACT]) ),
		( 1, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ BLUE, PINK, CYAN, ORANGE, GOLDEN, BROWN], (INPROGRESS, [ NO, NO, NO, NO, NO, NO]) ),
		( 1, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, MAROON, YELLOW, PURPLE, GREEN], (INPROGRESS, [ EXACT, EXACT, EXACT, NOTEXACT, NOTEXACT, NOTEXACT]) ),
		( 2, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], (WON, [ EXACT, EXACT, EXACT, EXACT, EXACT, EXACT]) ),
		( 1, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ BLUE, PINK, CYAN, ORANGE, GOLDEN, BROWN], (INPROGRESS, [ NO, NO, NO, NO, NO, NO]) ),
		( 20, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], (WON, [ EXACT, EXACT, EXACT, EXACT, EXACT, EXACT]) ),
		( 20, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ BLUE, PINK, CYAN, ORANGE, GOLDEN, BROWN], (LOST, [ NO, NO, NO, NO, NO, NO]) )
		
	])
	def test_playParameterizedAttemptsInTwentyRange(self, number_of_attempts, selected_colors, provided_colors, expected_result):
    	
		self.assertEqual(play(number_of_attempts, selected_colors, provided_colors), expected_result)


	@parameterized.expand([
		( 21, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW] ),
		( 21, [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW], [ BLUE, PINK, CYAN, ORANGE, GOLDEN, BROWN])
	])
	def test_playParameterizedAttemptsNotInTwentyRange(self, number_of_attempts, selected_colors, provided_colors):

		with self.assertRaises(Exception) as context:		
			play(number_of_attempts, selected_colors, provided_colors)

		self.assertEqual(str(context.exception), "Game already completed, start a new Game")

	def test_playwithColorsNotEqualToSix(self):

		with self.assertRaises(Exception) as context:		
			play(1, [ RED, GREEN, MAROON, PURPLE, YELLOW], [ WHITE, RED, GREEN, MAROON, PURPLE, YELLOW])

		self.assertTrue( str(context.exception) in ["Expecting 6 colors to be provided","Expecting 6 colors to be selected"] )

	def test_randomizedSelectedColorsEqual(self):
		result = select_distinct_colors()

		self.assertEqual(len(result), NUMBER_OF_COLORS)

		self.assertEqual(len(set(result)), NUMBER_OF_COLORS)

		self.assertTrue(all(color in AVAILABLE_COLORS_POOL.value for color in result ))

	def test_randomizedTwoConsecutiveCalls(self):
		first = select_distinct_colors()
		second = select_distinct_colors()

		self.assertNotEqual(first, second)
    

if __name__ == '__main__':  
  unittest.main()