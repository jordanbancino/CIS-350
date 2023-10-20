import random

import pygame

import graphics


class Obstacle:
    def __init__(self, img: pygame.Surface | pygame.SurfaceType,
                 rect: pygame.rect):
        self.img = img
        self.rect = rect

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect

    def draw(self, window, scale: (int, int)):
        img = pygame.transform.scale(self.img, scale[0], scale[1])
        window.blit(img, (self.rect.x, self.rect.y))
        # draws red box to show hitbox
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)


def create_random():
    # The list of assets we can choose from
    assets = [
        'calculator1.jpg',
        'rock.png'
    ]

    img = graphics.load_asset(random.choice(assets))
    rect = pygame.Rect(0, 0, 0, 0)

    return Obstacle(img, rect)
