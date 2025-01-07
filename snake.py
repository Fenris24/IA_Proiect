import pygame
import constants as const


class Snake:
    def __init__(self, position, direction, color, index, fill_index):
        self.position = position
        self.direction = direction
        self.color = color
        self.index = index
        self.fill_index = fill_index
        self.length = 0
        self.score = 0

    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != const.Dir.DOWN:
            self.direction = const.Dir.UP
        elif key == pygame.K_DOWN and self.direction != const.Dir.UP:
            self.direction = const.Dir.DOWN
        elif key == pygame.K_LEFT and self.direction != const.Dir.RIGHT:
            self.direction = const.Dir.LEFT
        elif key == pygame.K_RIGHT and self.direction != const.Dir.LEFT:
            self.direction = const.Dir.RIGHT

    def update(self):
        x, y = self.position
        if self.direction == const.Dir.UP and y > 0:
            self.length += 1
            self.position = (x, y - const.STRIDE)
        elif self.direction == const.Dir.DOWN and y < const.SCREEN_HEIGHT - const.STRIDE:
            self.length += 1
            self.position = (x, y + const.STRIDE)
        elif self.direction == const.Dir.LEFT and x > 0:
            self.length += 1
            self.position = (x - const.STRIDE, y)
        elif self.direction == const.Dir.RIGHT and x < const.SCREEN_WIDTH - const.STRIDE:
            self.length += 1
            self.position = (x + const.STRIDE, y)
        else:
            self.direction = const.Dir.NONE
