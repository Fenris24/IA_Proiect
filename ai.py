import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
import numpy as np
import functions as func


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
    return predictions[0].numpy()


def set_random_weights(model):
    for layer in model.layers:
        if layer.get_weights():
            weights_shape = layer.get_weights()[0].shape
            biases_shape = layer.get_weights()[1].shape
            random_weights = [
                np.random.uniform(-1, 1, weights_shape),
                np.random.uniform(-1, 1, biases_shape)
            ]
            layer.set_weights(random_weights)


def set_weights(model, weights):
    index = 0
    for layer in model.layers:
        if layer.get_weights():
            shapes = [w.shape for w in layer.get_weights()]
            num_params = [np.prod(shape) for shape in shapes]
            layer_weights = [
                np.array(weights[index:index + num_params[0]]).reshape(shapes[0]),
                np.array(weights[index + num_params[0]:index + sum(num_params)]).reshape(shapes[1])
            ]
            layer.set_weights(layer_weights)
            index += sum(num_params)


def save_weights(model, file_name):
    weights = [layer.get_weights() for layer in model.layers if layer.get_weights()]
    np.save(file_name, weights, allow_pickle=True)


def load_flat_weights(model, file_name):
    flat_weights = np.load(file_name)

    expected_shapes = [w.shape for layer in model.layers for w in layer.get_weights()]
    num_params = [np.prod(shape) for shape in expected_shapes]

    if len(flat_weights) != sum(num_params):
        raise ValueError(f"Mismatch in total weights: expected {sum(num_params)}, got {len(flat_weights)}")

    reshaped_weights = []
    idx = 0
    for shape, size in zip(expected_shapes, num_params):
        reshaped_weights.append(flat_weights[idx:idx + size].reshape(shape))
        idx += size

    model.set_weights(reshaped_weights)