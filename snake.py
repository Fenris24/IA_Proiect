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
        self.fill_score = 0
        self.is_dead = False
        self.history = []

    def kill(self):
        self.score = -2000
        self.is_dead = True

    def update_history(self):
        if len(self.history) >= 4:
            self.history.pop(0)
        self.history.append(self.direction)

    def detect_circle(self):
        clockwise = [const.Dir.UP, const.Dir.RIGHT, const.Dir.DOWN, const.Dir.LEFT]
        counterclockwise = [const.Dir.UP, const.Dir.LEFT, const.Dir.DOWN, const.Dir.RIGHT]

        if len(self.history) < 4:
            return

        for i in range(4):
            rotated_history = self.history[i:] + self.history[:i]
            if rotated_history == clockwise or rotated_history == counterclockwise:
                self.score += 10000
                print('ROTATEEEEEEED')
                self.history = []
                break

    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != const.Dir.DOWN:
            self.direction = const.Dir.UP
        elif key == pygame.K_DOWN and self.direction != const.Dir.UP:
            self.direction = const.Dir.DOWN
        elif key == pygame.K_LEFT and self.direction != const.Dir.RIGHT:
            self.direction = const.Dir.LEFT
        elif key == pygame.K_RIGHT and self.direction != const.Dir.LEFT:
            self.direction = const.Dir.RIGHT

    def change_ai_direction(self, direction):
        if direction == const.Dir.UP and self.direction != const.Dir.DOWN:
            self.direction = const.Dir.UP
        elif direction == const.Dir.DOWN and self.direction != const.Dir.UP:
            self.direction = const.Dir.DOWN
        elif direction == const.Dir.LEFT and self.direction != const.Dir.RIGHT:
            self.direction = const.Dir.LEFT
        elif direction == const.Dir.RIGHT and self.direction != const.Dir.LEFT:
            self.direction = const.Dir.RIGHT

        self.update_history()
        self.detect_circle()

    def update(self):
        x, y = self.position

        if self.direction == const.Dir.UP:
            # if y > const.STRIDE:
            self.length += 1
            y = (y - const.STRIDE) % const.SCREEN_HEIGHT
            self.position = (x, y)
            # else:
            #     self.score -= 300
        elif self.direction == const.Dir.DOWN:
            # if y < const.SCREEN_HEIGHT - const.STRIDE:
            self.length += 1
            y = (y + const.STRIDE) % const.SCREEN_HEIGHT
            self.position = (x, y)
            # else:
            #     self.score -= 300
        elif self.direction == const.Dir.LEFT:
            # if x > const.STRIDE:
            self.length += 1
            x = (x - const.STRIDE) % const.SCREEN_WIDTH
            self.position = (x, y)
            # else:
            #     self.score -= 300
        elif self.direction == const.Dir.RIGHT:
            #if x < const.SCREEN_WIDTH - const.STRIDE:
            self.length += 1
            x = (x + const.STRIDE) % const.SCREEN_WIDTH
            self.position = (x, y)
            # else:
            #     self.score -= 300
