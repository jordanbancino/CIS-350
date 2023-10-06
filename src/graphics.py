"""
graphics module:
"""
import pygame
import os

pygame.font.init()  # initialize pygame's font module

# CONSTANTS
width, height = 900, 500  # window width and height
font_size = 20  # size of the text

# COMPONENTS
window = pygame.display.set_mode((width, height))  # create window and set size
pygame.display.set_caption("ARG")  # set window title
score = 0 #current score

background_image = pygame.image.load(os.path.join('assets', "background.png"))  # set background
background = pygame.transform.scale(background_image, (width, height))  # scale correctly

character_image = pygame.image.load(os.path.join('assets', "stickman.png"))  # create character image
character = pygame.transform.scale(character_image, (100, 100))  # resize character image
stickman = pygame.Rect(300, 315, 100, 100)  # makes a rectangle that is the size of the stickman

font = pygame.font.SysFont("comicsans", font_size)  # changes font for text
pause_info = font.render("Press SPACEBAR To Pause", True, "black")  # antialias makes text look better
score_info = font.render("SCORE: " + str(score), True, "black")

def update_ui(window) -> None:
    """
	Sets UI, displays the bit that doesn't need to be updated each frame (for now).
	char is the parameter that represents the properties of the character.
	"""
    window.blit(background, (0, 0))  # displays background image
    # set pause_info text on top right with 5x5 px padding
    window.blit(pause_info, (width - pause_info.get_width() - 5, 5))  # blit pause_info post background to be front
    window.blit(score_info, (350, 5))
    window.blit(character, (stickman.x, stickman.y))  # displays the character at a position
    pygame.display.update()  # let set graphics (via blit, draw, etc.) take effect