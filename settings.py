import random
import pygame
from pygame.math import Vector2 as vec
from sys import exit

CELL_SIZE = 128
CELL_NUMBER = 5


PUZZLE_DATA = {  # x y
    'yellow': [vec(0, 0), vec(3, 3)],
    'green': [vec(4, 0), vec(3, 1)],
    'purple': [vec(1, 1), vec(0, 3)],
    'blue': [vec(1, 2), vec(3, 2)],
}

COLOR = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}

ALPHA_VALUE_OVERLAY = 170
