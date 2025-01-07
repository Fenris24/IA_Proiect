import pygame
import sys
import ai
import snake as entity
import functions as fun
import constants as const


def game(time_limit):
    timer = 0
    snakes = []
    max_width = const.SCREEN_WIDTH - const.STRIDE
    max_height = const.SCREEN_HEIGHT - const.STRIDE
    snakes.append(entity.Snake((0, 0), const.Dir.RIGHT, const.RED, 1, 2))
    snakes.append(entity.Snake((max_width, 0), const.Dir.DOWN, const.GREEN, 3, 4))
    snakes.append(entity.Snake((max_width, max_height), const.Dir.LEFT, const.BLUE, 5, 6))
    snakes.append(entity.Snake((0, max_height), const.Dir.UP, const.YELLOW, 7, 8))
    grid = [[0 for _ in range(const.GRID_WIDTH)] for _ in range(const.GRID_HEIGHT)]
    frame_count = 0
    running = True
    model = ai.create_model(const.GRID_WIDTH * const.GRID_HEIGHT + 4 + 1)

    while running:
        frame_count += 1
        timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # snake.change_direction(event.key)
        for snake in snakes:
            snake.direction = ai.predict_move(model, grid, snake)
            print(snake.direction)
        if frame_count % const.UPDATE_RATE == 0:
            for snake in snakes:
                snake.update()
                y, x = snake.position
                if (grid[x // const.STRIDE][y // const.STRIDE] == snake.index or
                    grid[x // const.STRIDE][y // const.STRIDE] == snake.fill_index) and\
                        snake.direction != const.Dir.NONE:
                    fun.flood_fill(grid, snake.index, snake.fill_index)
                    snake.length = 0
                grid[x // const.STRIDE][y // const.STRIDE] = -snake.index
            if not const.SIMULATION:
                const.screen.fill(const.BLACK)
            fun.draw_grid(grid, snakes)
        if not const.SIMULATION:
            pygame.display.flip()

        const.clock.tick(const.FPS)
        if frame_count > const.FPS:
            frame_count = 0
        if timer > time_limit:
            running = False

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    game(300)
