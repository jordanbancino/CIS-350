"""
arg module: where the game lives
"""
import pygame
import os
pygame.font.init()  # initialize pygame's font module

# CONSTANTS
width, height = 900, 500  # window width and height
fps = 120
font_size = 20

# COMPONENTS
window = pygame.display.set_mode((width, height)) # create window and set size
pygame.display.set_caption("ARG") # set window title
background_image = pygame.image.load(os.path.join('..', 'assets', "background.png")) # set background
background_image = pygame.transform.scale(background_image, (width, height)) # scale correctly
font = pygame.font.SysFont("comicsans", font_size)
pause_info = font.render("Press SPACEBAR to pause.", True, "black") # antialias makes text look better

def set_ui():
	"""
	Sets UI, displays the bit that doesn't need to be updated each frame (for now).
	"""
	window.blit(background_image, (0, 0))
	# set pause_info text on top right with 5x5 px padding
	window.blit(pause_info, (width - pause_info.get_width() - 5, 5)) # blit pause_info post background to be front
	pygame.display.update() # let set graphics (via blit, draw, etc.) take effect


def main():
	"""
	The game entry function. All initial setup and final teardown
	happens here; this function is always the first pushed on the
	stack and that last popped off, at which point the program
	exits.
	"""
	clock = pygame.time.Clock() # keep track of time
	set_ui()
	program_running = True
	while program_running:
		clock.tick(fps)  # run while-loop at a max rate of fps
		for event in pygame.event.get(): # iterate over all occurred events since last while-loop iteration
			if event.type == pygame.QUIT: # if user pressed window's "X"
				program_running = False  # time to exit while-loop
				break  # break for-loop, no need to check remaining events
	pygame.quit() # close window, end program


if __name__ == "__main__":
	main()