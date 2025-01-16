from stat import FILE_ATTRIBUTE_INTEGRITY_STREAM
from xml.etree.ElementTree import tostring

import pygame
from enum import Enum

from pygame.image import tostring

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
STRIDE = 40
GRID_WIDTH = SCREEN_WIDTH // STRIDE
GRID_HEIGHT = SCREEN_HEIGHT // STRIDE
FPS = 60
UPDATE_RATE = 1
SIMULATION = False
SIMULATION_TIME = 200
TRAINING = False

F1 = 25
F2 = 26
FILE_IN = "generations/best_weights_gen_" + str(F1) + ".npy"
FILE_OUT = "generations/best_weights_gen_" + str(F2) + ".npy"

CR = 0.9
F = 0.8 - F1 / 1000
POP_SIZE = 40
INPUTS = (GRID_WIDTH * GRID_HEIGHT + 4 + 2 + 1)
LAYER_1 = INPUTS * 64 + 64
LAYER_2 = 64 * 32 + 32
LAYER_3 = 32 * 4 + 4
WEIGHTS_SIZE = LAYER_1 + LAYER_2 + LAYER_3
NR_SNAKES = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRID = (100, 100, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Battles")
clock = pygame.time.Clock()


class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NONE = 4
