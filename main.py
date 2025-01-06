import pygame
import sys
from enum import Enum

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
STRIDE = 20
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
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


class Snake:
    def __init__(self, position, direction, color, index):
        self.position = position
        self.direction = direction
        self.color = color
        self.index = index

    def change_direction(self, key):
        if key == pygame.K_UP and self.direction != Dir.DOWN:
            self.direction = Dir.UP
        elif key == pygame.K_DOWN and self.direction != Dir.UP:
            self.direction = Dir.DOWN
        elif key == pygame.K_LEFT and self.direction != Dir.RIGHT:
            self.direction = Dir.LEFT
        elif key == pygame.K_RIGHT and self.direction != Dir.LEFT:
            self.direction = Dir.RIGHT

    def update(self):
        x, y = self.position
        if self.direction == Dir.UP and y > 0:
            self.position = (x, y - STRIDE)
        elif self.direction == Dir.DOWN and y < SCREEN_HEIGHT - STRIDE:
            self.position = (x, y + STRIDE)
        elif self.direction == Dir.LEFT and x > 0:
            self.position = (x - STRIDE, y)
        elif self.direction == Dir.RIGHT and x < SCREEN_WIDTH - STRIDE:
            self.position = (x + STRIDE, y)
        else:
            self.direction = Dir.NONE


def flood_fill(grid, snake_index):
    from collections import deque

    rows = len(grid)
    cols = len(grid[0])
    queue = deque()

    for x in range(cols):
        queue.append((x, 0))
        queue.append((x, rows - 1))
    for y in range(rows):
        queue.append((0, y))
        queue.append((cols - 1, y))

    while queue:
        x, y = queue.popleft()
        if x < 0 or x >= cols or y < 0 or y >= rows:
            continue
        if grid[y][x] != 0:
            continue
        grid[y][x] = 99

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0:
                grid[y][x] = snake_index

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 99:
                grid[y][x] = 0


def draw_grid(grid, index):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * STRIDE, y * STRIDE, STRIDE, STRIDE)
            if cell == index:
                pygame.draw.rect(screen, RED, rect)
            elif cell == -index:
                darker_red = (RED[0] - 80, 0, 0)
                pygame.draw.rect(screen, darker_red, rect)
                grid[y][x] = index
            pygame.draw.rect(screen, GRID, rect, 1)


def game():
    snake = Snake((0, 0), Dir.DOWN, RED, 1)
    grid = [[0 for _ in range(SCREEN_WIDTH // STRIDE)] for _ in range(SCREEN_HEIGHT // STRIDE)]
    frame_count = 0
    running = True

    while running:
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                snake.change_direction(event.key)

        if frame_count % 10 == 0:
            snake.update()
            y, x = snake.position
            if grid[x // STRIDE][y // STRIDE] == snake.index:
                flood_fill(grid, snake.index)
            grid[x // STRIDE][y // STRIDE] = -snake.index
            screen.fill(BLACK)
            draw_grid(grid, snake.index)

        pygame.display.flip()

        clock.tick(FPS)
        if frame_count > 60:
            frame_count = 0

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    game()
