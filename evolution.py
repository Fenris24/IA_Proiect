import game
import ai
import os
import constants as const
import numpy as np


def initialize_population():
    population = []
    if os.path.exists(const.FILE_IN):
        best_weights = np.load(const.FILE_IN)
        population.append(best_weights)

    while len(population) < const.POP_SIZE:
        population.append(np.random.uniform(-1, 1, const.WEIGHTS_SIZE))

    return population


def mutation(population, target):
    indices = list(range(len(population)))
    indices.remove(target)
    r1, r2, r3 = np.random.choice(indices, 3, replace=False)
    individual = population[r1] + const.F * (population[r2] - population[r3])
    return individual


def crossover(target, mutant):
    trial = np.copy(target)
    for j in range(len(target)):
        if np.random.rand() < const.CR or j == np.random.randint(len(target)):
            trial[j] = mutant[j]
    return trial


def selection(weights):
    fitness_scores = []
    for i in range(0, len(weights), const.NR_SNAKES):
        chunk = weights[i:i + const.NR_SNAKES]
        models = []
        for model_weights in chunk:
            model = ai.create_model(const.INPUTS)
            ai.set_weights(model, model_weights)
            models.append(model)
        scores = game.run(models)
        fitness_scores.extend(scores[:len(chunk)])
        # print(f"simulation {(i / 4 ) + 1} completed with the scores:{fitness_scores[-4:]}")
    return fitness_scores


def differential_evolution(epochs):
    population = initialize_population()
    for epoch in range(epochs):
        new_population = []
        fitness_scores = selection(population)
        for i in range(const.POP_SIZE):
            # print("mutation in progress...")
            individual = mutation(population, i)
            # print("mutation complete.")

            # print("crossover in progress...")
            trial = crossover(population[i], individual)
            trial_population = population[:const.NR_SNAKES - 1]
            trial_population.append(trial)
            # print("crossover complete.")

            # print("selection in progress...")
            trial_scores = selection(trial_population)
            trial_fitness = trial_scores[-1]
            if trial_fitness > fitness_scores[i]:
                new_population.append(trial)
            else:
                new_population.append(population[i])
            # print("selection complete.")
        population = new_population
        best_fitness = max(fitness_scores)
        print(f"Epoch {epoch + 1}/{epochs}, best fitness: {best_fitness}")
    fitness_scores = selection(population)
    best_index = np.argmax(fitness_scores)
    best_weights = population[best_index]
    np.save(const.FILE_OUT, best_weights)
    print(f"generation {const.F2}")
