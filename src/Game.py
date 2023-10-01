"""
This is the Game module.
"""
import Log
import pygame
import pygame_gui


class Game():
	"""
	A Game object, which consists of a single main function.
	"""
	pygame.init()
	width, height = 900, 500
	display = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Solve Arithmetic Game")
	# background initiating code
	background = pygame.image.load("background.png")
	fps = 60

	def main(self) -> int:
		"""
		The game entry function. All initial setup and final teardown
		happens here; this function is always the first pushed on the
		stack and that last popped off, at which point the program
		exits.
		"""

		Log.msg(Log.INFO, "Starting...")
		Log.msg(Log.DEBUG, "Initializing pygame...")
		# pygame startup
		loop_speed = pygame.time.Clock()
		program_running = True
		while program_running:
			loop_speed.tick(Game.fps)
			# attempt to make background appear
			Game.display.blit(Game.background, (0, 0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					program_running = False

		pygame.quit()

		return 0
