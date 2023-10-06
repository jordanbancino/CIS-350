"""
arg module: where the game lives
"""
import pygame
import os
import arithmetic
pygame.font.init()  # initialize pygame's font module

# CONSTANTS
width, height = 900, 500  # window width and height
fps = 120 # frames per second
font_size = 20 # size of the text

# COMPONENTS
window = pygame.display.set_mode((width, height)) # create window and set size
pygame.display.set_caption("ARG") # set window title
menu_border_image = pygame.image.load(os.path.join('assets', "menu_border.png")) # set menu border
menu_border = pygame.transform.scale(menu_border_image, (width, height)) # scale correctly

background_image = pygame.image.load(os.path.join('assets', "background.png")) # set background
background = pygame.transform.scale(background_image, (width, height)) # scale correctly

font = pygame.font.SysFont("comicsans", font_size) # changes font for text
pause_info = font.render("Press SPACEBAR to pause.", True, "black") # antialias makes text look better

character_image = pygame.image.load(os.path.join('assets', "stickman.png")) # create character image
character = pygame.transform.scale(character_image, (100, 100)) # resize character image

start_button_img = pygame.image.load(os.path.join('assets', 'start_button.png')) # create start button

score_button_img = pygame.image.load(os.path.join('assets', 'score_button.png')) # create score button

quit_button_img = pygame.image.load(os.path.join('assets', 'quit_button.png')) # create quit button

class Button():
	def __init__(self, x, y, image):
		self.image = pygame.transform.scale(image, (200, 100))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
	def draw(self):

		action = False
		#get mouse pos
		pos = pygame.mouse.get_pos()
		#check mouse over button and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False
		#draw button on screen
		window.blit(self.image, (self.rect.x, self.rect.y))

		return action
	
#create button instances
start_button = Button(350, 75, start_button_img)
score_button = Button(350, 200, score_button_img)
quit_button = Button(350, 325, quit_button_img)

def set_main_menu():
	window.fill((47, 79, 79)) # make screen gray
	window.blit(menu_border, (0, 0)) # display border
	start_button.draw()
	score_button.draw()
	quit_button.draw()
	pygame.display.update()

def set_ui(char) -> None:
	"""
	Sets UI, displays the bit that doesn't need to be updated each frame (for now).
	char is the parameter that represents the properties of the character.
	"""
	window.blit(background, (0, 0)) # displays background image
	# set pause_info text on top right with 5x5 px padding
	window.blit(pause_info, (width - pause_info.get_width() - 5, 5)) # blit pause_info post background to be front
	window.blit(character, (char.x, char.y)) # displays the character at a position
	pygame.display.update() # let set graphics (via blit, draw, etc.) take effect

def main() -> None:
	"""
	The game entry function. All initial setup and final teardown
	happens here; this function is always the first pushed on the
	stack and that last popped off, at which point the program
	exits.
	"""
	clock = pygame.time.Clock() # keep track of time
	stickman = pygame.Rect(300, 315, 100, 100) # makes a rectangle that is the size of the stickman
	set_main_menu()
	program_running = True
	while program_running:
		clock.tick(fps)  # run while-loop at a max rate of fps
		if start_button.draw():
			set_ui(stickman)
			stickman.x += 1 # character moves 1 pixel per frame
		if quit_button.draw():
			program_running = False
		for event in pygame.event.get(): # iterate over all occurred events since last while-loop iteration
			if event.type == pygame.QUIT: # if user pressed window's "X"
				program_running = False  # time to exit while-loop
				break  # break for-loop, no need to check remaining events

	pygame.quit() # close window, end program


if __name__ == "__main__":
	main()
