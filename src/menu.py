"""
menu module: components of main and pause menus and end screen
"""
import pygame
import os

width, height = 900, 500  # window width and height

menu_border_image = pygame.image.load(os.path.join('assets', "menu_border.png"))  # set menu border
menu_border = pygame.transform.scale(menu_border_image, (width, height))  # scale correctly

start_button_img = pygame.image.load(os.path.join('assets', 'start_button.png'))  # create start button
score_button_img = pygame.image.load(os.path.join('assets', 'score_button.png'))  # create score button
quit_button_img = pygame.image.load(os.path.join('assets', 'quit_button.png'))  # create quit button


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (200, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, window):
        """
        Draws a button on the display and monitors clicking.
        """
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        # check mouse over button and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        # draw button on screen
        window.blit(self.image, (self.rect.x, self.rect.y))

        return action

# create button instances
start_button = Button(350, 75, start_button_img)
score_button = Button(350, 200, score_button_img)
quit_button = Button(350, 325, quit_button_img)
buttons = [start_button, score_button, quit_button]

def set_main_menu(window):
    window.fill((47, 79, 79))  # make screen gray
    window.blit(menu_border, (0, 0))  # display border
    for button in buttons:
        button.draw(window)
    pygame.display.update()

def in_main_menu(window) -> bool:
    """
    Determines if user started game (True) or exited window (False).
    """
    if quit_button.draw(window):
        pygame.quit()  # close window, end program
        return False
