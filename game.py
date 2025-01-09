import pygame
import ai
import snake as entity
import functions as fun
import constants as const
import random


def run(models):
    timer = 0
    snakes = []
    max_width = const.SCREEN_WIDTH - const.STRIDE
    max_height = const.SCREEN_HEIGHT - const.STRIDE
    x = random.randint(0, max_width // 2)
    y = random.randint(0, max_height // 2)
    snakes.append(entity.Snake((x, y), const.Dir.RIGHT, const.RED, 1, 2))
    x = random.randint(max_width // 2, max_width)
    y = random.randint(0, max_height // 2)
    snakes.append(entity.Snake((x, y), const.Dir.DOWN, const.GREEN, 3, 4))
    x = random.randint(max_width // 2, max_width)
    y = random.randint(max_height // 2, max_height)
    snakes.append(entity.Snake((x, y), const.Dir.LEFT, const.BLUE, 5, 6))
    x = random.randint(0, max_width // 2)
    y = random.randint(max_height // 2, max_height)
    snakes.append(entity.Snake((x, y), const.Dir.UP, const.YELLOW, 7, 8))
    grid = [[0 for _ in range(const.GRID_WIDTH)] for _ in range(const.GRID_HEIGHT)]
    frame_count = 0
    running = True

    while running:
        frame_count += 1
        timer += 1
        if not const.SIMULATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    snakes[0].change_direction(event.key)
        if const.TRAINING:
            for i in range(4):
                predicted_direction = ai.predict_move(models[i], grid, snakes[i])
                x, y = snakes[i].position
                if (predicted_direction == const.Dir.UP and y <= const.STRIDE) or \
                        (predicted_direction == const.Dir.DOWN and y >= const.SCREEN_HEIGHT - const.STRIDE) or \
                        (predicted_direction == const.Dir.LEFT and x <= const.STRIDE) or \
                        (predicted_direction == const.Dir.RIGHT and x >= const.SCREEN_WIDTH - const.STRIDE):
                    snakes[i].score -= 100
                else:
                    snakes[i].change_ai_direction(predicted_direction)
            # print(f'snake{i} moves: {snakes[i].direction}')
        if frame_count % const.UPDATE_RATE == 0:
            for snake in snakes:
                if not snake.is_dead:
                    snake.update()
                    y, x = snake.position
                    if (grid[x // const.STRIDE][y // const.STRIDE] == snake.index or
                        grid[x // const.STRIDE][y // const.STRIDE] == snake.fill_index) and\
                            snake.direction != const.Dir.NONE:
                        snake.fill_score = fun.flood_fill(grid, snake.index, snake.fill_index)
                        snake.length = 0
                    elif (grid[x // const.STRIDE][y // const.STRIDE] != snake.index and
                            grid[x // const.STRIDE][y // const.STRIDE] != snake.fill_index and
                            grid[x // const.STRIDE][y // const.STRIDE] != 0 and
                            grid[x // const.STRIDE][y // const.STRIDE] % 2 != 0):
                        for s in snakes:
                            if s.index == grid[x // const.STRIDE][y // const.STRIDE]:
                                s.kill()
                    grid[x // const.STRIDE][y // const.STRIDE] = -snake.index
            if not const.SIMULATION:
                const.screen.fill(const.BLACK)
            fun.draw_grid(grid, snakes)
        if not const.SIMULATION:
            pygame.display.flip()

        const.clock.tick(const.FPS)
        if frame_count > const.FPS:
            frame_count = 0
        if timer > const.SIMULATION_TIME:
            running = False
    for snake in snakes:
        snake.score += snake.fill_score * 2
    return [snake.score for snake in snakes]
