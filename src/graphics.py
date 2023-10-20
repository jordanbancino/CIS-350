"""
graphics module:
"""
import os

import pygame


def load_asset(asset: str) -> pygame.Surface | pygame.SurfaceType:
    path = os.path.join('assets', asset)
    return pygame.image.load(path)
