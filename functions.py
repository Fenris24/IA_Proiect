import pygame
import constants as const
from collections import deque


def flood_fill(grid, index, fill_index):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque()

    for x in range(cols):
        if grid[0][x] != index or grid[0][x] != fill_index:
            queue.append((x, 0))
        if grid[rows - 1][x] != index or grid[rows - 1][x] != fill_index:
            queue.append((x, rows - 1))
    for y in range(rows):
        if grid[y][0] != index or grid[y][0] != fill_index:
            queue.append((0, y))
        if grid[y][cols - 1] != index or grid[y][cols - 1] != fill_index:
            queue.append((cols - 1, y))

    while queue:
        x, y = queue.popleft()
        if x < 0 or x >= cols or y < 0 or y >= rows:
            continue
        if visited[y][x]:
            continue
        if grid[y][x] == index or grid[y][x] == fill_index:
            continue
        visited[y][x] = True

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))

    score = 0
    for y in range(rows):
        for x in range(cols):
            if not visited[y][x]:
                grid[y][x] = fill_index
                score += 1
    return score


def draw_grid(grid, snakes):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * const.STRIDE, y * const.STRIDE, const.STRIDE, const.STRIDE)
            for snake in snakes:
                if not snake.is_dead:
                    if cell == snake.index:
                        if not const.SIMULATION:
                            pygame.draw.rect(const.screen, snake.color, rect)
                    elif cell == snake.fill_index:
                        if not const.SIMULATION:
                            pygame.draw.rect(const.screen, snake.color, rect)
                    elif cell == -snake.index:
                        darker_color = tuple(max(0, int(c * 0.8)) for c in snake.color)
                        if not const.SIMULATION:
                            pygame.draw.rect(const.screen, darker_color, rect)
                        grid[y][x] = snake.index
            if not const.SIMULATION:
                pygame.draw.rect(const.screen, const.GRID, rect, 1)


def get_data(grid, snake):
    normalized_grid = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                normalized_grid.append(0.0)
            elif cell == snake.index:
                normalized_grid.append(0.25)
            elif cell == snake.fill_index:
                normalized_grid.append(0.5)
            elif cell % 2 == 0:
                normalized_grid.append(0.75)
            else:
                normalized_grid.append(1.0)
    direction = [0, 0, 0, 0]
    if snake.direction == const.Dir.UP:
        direction[0] = 1
    elif snake.direction == const.Dir.DOWN:
        direction[1] = 1
    elif snake.direction == const.Dir.LEFT:
        direction[2] = 1
    elif snake.direction == const.Dir.RIGHT:
        direction[3] = 1
    x, y = snake.position
    x_normalized = x / (const.SCREEN_WIDTH - 1)
    y_normalized = y / (const.SCREEN_HEIGHT - 1)
    return normalized_grid + direction + [x_normalized, y_normalized] + [snake.length]
