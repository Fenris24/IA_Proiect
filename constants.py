import pygame
from enum import Enum

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
STRIDE = 20
GRID_WIDTH = SCREEN_WIDTH // STRIDE
GRID_HEIGHT = SCREEN_HEIGHT // STRIDE
FPS = 60
UPDATE_RATE = 1
SIMULATION = False

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
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NONE = 0
