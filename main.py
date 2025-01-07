import pygame
import game
import os
import ai
import evolution as ev
import constants as const


if __name__ == '__main__':
    pygame.init()
    const.SIMULATION = False
    const.FPS = 240
    const.SIMULATION_TIME = 120
    training = True
    if training:
        ev.differential_evolution(10)
    else:
        models = []
        for i in range(4):
            models.append(ai.create_model(const.WEIGHTS_SIZE))
            file_name = 'best_weights.npy'
            if os.path.exists(file_name):
                ai.load_weights(models[i], file_name)
            else:
                ai.set_random_weights(models[i])
        const.SIMULATION_TIME = 100000
        const.UPDATE_RATE = 10
        game.run(models)
    pygame.quit()
