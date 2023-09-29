"""
This is the Game module.
"""

import Log

class Game():
	"""
	A Game object, which consists of a single main function.
	"""

	def main(self) -> int:
		"""
		The game entry function. All initial setup and final teardown
		happens here; this function is aways the first pushed on the
		stack and that last popped off, at which point the program
		exits.
		"""

		Log.msg(Log.INFO, "Starting...")
		Log.msg(Log.DEBUG, "Initializing pygame...")

		return 0
