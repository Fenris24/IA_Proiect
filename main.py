import pygame
import game
import os
import ai
import evolution as ev
import constants as const


if __name__ == '__main__':
    pygame.init()
    const.SIMULATION = False
    const.FPS = 360
    const.SIMULATION_TIME = 360
    const.TRAINING = True
    if const.TRAINING:
        for i in range(100):
            ev.differential_evolution(10)
            const.F1 += 1
            const.F2 += 1
            const.FILE_IN = "generations/best_weights_gen_" + str(const.F1) + ".npy"
            const.FILE_OUT = "generations/best_weights_gen_" + str(const.F2) + ".npy"
            const.F -= 0.001
    else:
        models = []
        for i in range(4):
            models.append(ai.create_model(const.INPUTS))
            file_name = "generations/best_weights_gen_" + str(const.F2) + ".npy"
            if os.path.exists(file_name):
                ai.load_flat_weights(models[i], file_name)
            else:
                ai.set_random_weights(models[i])
        const.SIMULATION_TIME = 100000
        const.UPDATE_RATE = 10
        game.run(models)
    pygame.quit()
