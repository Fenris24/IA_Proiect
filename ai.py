import tensorflow as tf
from tensorflow.keras import layers
import functions as func
import constants as const


def create_model(input_size):
    model = tf.keras.Sequential([
        layers.Input(shape=(input_size,)),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(4, activation='softmax')
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
