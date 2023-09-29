"""
This is the Game module.
"""

class Game():
	"""
	A Game object, which consists of a single main function.
	"""

	def main(self):
		"""
		The game entry function. All initial setup and final teardown
		happens here; this function is aways the first pushed on the
		stack and that last popped off, at which point the program
		exits.
		"""
		print("Game main")

