import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
import numpy as np
import functions as func
import constants as const


def create_model(input_size):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_size,)),
        Dense(32, activation='relu'),
        Dense(4, activation='softmax')
    ])
    return model


def predict_move(model, grid, snake):
    data = func.get_data(grid, snake)
    data = tf.convert_to_tensor([data])
    predictions = model(data)
    move = tf.argmax(predictions[0]).numpy()
    if move == 0:
        return const.Dir.UP
    elif move == 1:
        return const.Dir.DOWN
    elif move == 2:
        return const.Dir.LEFT
    elif move == 3:
        return const.Dir.RIGHT


def generate_random_weights(model):
    random_weights = []
    for layer in model.layers:
        weights_shape = layer.get_weights()[0].shape
        random_weights.append(np.random.uniform(-1, 1, weights_shape))
    return random_weights


def set_random_weights(model):
    for layer in model.layers:
        if layer.get_weights():
            weights_shape = layer.get_weights()[0].shape
            random_weights = [
                np.random.uniform(-1, 1, weights_shape),
            ]
            layer.set_weights(random_weights)


def set_weights(model, weights):
    idx = 0
    for layer in model.layers:
        if layer.get_weights():
            shapes = [w.shape for w in layer.get_weights()]
            num_params = [np.prod(shape) for shape in shapes]
            layer_weights = [
                np.array(weights[idx:idx + num_params[0]]).reshape(shapes[0]),
                np.array(weights[idx + num_params[0]:idx + sum(num_params)]).reshape(shapes[1])
            ]
            layer.set_weights(layer_weights)
            idx += sum(num_params)


def save_weights(model, file_name):
    weights = [layer.get_weights() for layer in model.layers if layer.get_weights()]
    np.save(file_name, weights)


def load_weights(model, file_name):
    weights = np.load(file_name, allow_pickle=True)
    for layer, layer_weights in zip(model.layers, weights):
        layer.set_weights(layer_weights)
