import pygame
from src import graphics
import random


# idk what the first argument of this is, the video puts USREVENT+2 if that helps figure out what it is.
# I think it's calling a specific event but im not sure where that part goes.
pygame.time.set_timer(IDK, random.randrange(2000, 3500))  #


class Obstacle(object):
    img = []

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit_box = (x, y, width, height)


class Obstacle1(Obstacle):
    img = [graphics.load_asset('Obstacle1.png')]

    def draw(self, window):
        self.hit_box = (self.x, self.y, self.width, self.height)
        window.blit(self.img, (self.x, self.y))
        pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2) # draws red box to show hitbox


class Obstacle2(Obstacle):
    img = [graphics.load_asset('Obstacle2.png')]

    def draw(self, window):
        self.hit_box = (self.x, self.y, self.width, self.height)
        window.blit(self.img, (self.x, self.y))
        pygame.draw.rect(window, (255, 0, 0), self.hit_box, 2)  # draws red box to show hitbox


def redraw_window():  # should draw the objects on the window.
    for x in objects:
        x.draw(window)
    pygame.display.update()


objects = []

# this next bit of code goes under the events for loop in arg, it's what chooses which object to create next.
# Calls teh unknown event created before.
# Set up to be easily increase-able as time goes on and we make more objects..
if event.type == IDK:
    r = random.randrange(0, 2)
    if r == 0:
        objects.append(Obstacle1(810, 315, 100, 100))
    else:
        objects.append(Obstacle2(810, 315, 100, 100))
