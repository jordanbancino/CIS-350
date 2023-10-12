"""
graphics module: TODO: merge with another module
"""
import pygame
import os


def load_asset(asset: str) -> pygame.Surface:
    path = os.path.join('assets', asset)
    return pygame.image.load(path)
