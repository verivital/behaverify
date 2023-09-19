'''
Just a quick think to train the x portion of the xy net to test whether or not we can encode it effectively.
'''
import os
import tensorflow as tf
import numpy
from tensorflow import keras

from keras.utils import plot_model
from graphviz import Digraph


class StopOnPoint(tf.keras.callbacks.Callback):
    def __init__(self, point):
        super(StopOnPoint, self).__init__()
        self.point = point

    def on_epoch_end(self, epoch, logs=None): 
        accuracy = logs["accuracy"]
        if accuracy >= self.point:
            self.model.stop_training = True

#callbacks = [StopOnPoint(0.98)] # <- set optimal point


# we assume [x1, x0] means current location, previous destination.
def convert_to_array(label, x_min, x_max):
    array_label = [0] * (x_max + 1 - x_min)
    array_label[label] = 1
    return array_label

def create_labeled_dataset(x_min, x_max):
    x_mid = (x_max + x_min)/2
    input_data = [[x1, x2] for x1 in range(x_min, x_max + 1) for x2 in range(x_min, x_max + 1)]
    #labels = list(map(lambda input_vals: ((x_min if input_vals[1] >= x_mid else x_max) if input_vals[0] == input_vals[1] else input_vals[0]), input_data))
    labels = list(map(lambda input_vals: convert_to_array(((x_min if input_vals[1] >= x_mid else x_max) if input_vals[0] == input_vals[1] else input_vals[0]), x_min, x_max), input_data))
    return (numpy.array(input_data), numpy.array(labels))

def train_model(input_dim, output_dim, input_data, labels, epochs, batch_size):
    # Create a neural network model
    model = keras.Sequential([
        keras.layers.Dense(10, activation='relu', input_shape=(input_dim,)),  # Replace input_dim with your input dimension
        keras.layers.Dense(10, activation='relu'),
        keras.layers.Dense(10, activation='relu'),
        keras.layers.Dense(10, activation='relu'),
        keras.layers.Dense(output_dim, activation='softmax')  # Replace output_dim with your output dimension
    ])
    # Compile the model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',  # Use appropriate loss function for your problem
                  metrics=['accuracy'])
    # Train the model
    model.fit(input_data, labels, epochs=epochs, batch_size=batch_size, callbacks = [StopOnPoint(0.999)])
    return model

def recursive_max(cur_node, layer_index):
    return (
        ''
        if cur_node < 0
        else
        (
            ('x_net_node_' + str(layer_index) + '_' + str(cur_node))
            if cur_node == 0
            else
            (
                ('(max, ' + 'x_net_node_' + str(layer_index) + '_' + str(cur_node) + ', ' +  'x_net_node_' + str(layer_index) + '_' + str(cur_node - 1) + ')')
                if cur_node == 1
                else
                (
                    '(max, ' + 'x_net_node_' + str(layer_index) + '_' + str(cur_node) + ', ' + recursive_max(cur_node - 1, layer_index) + ')'
                )
            )
        )
    )

def idk():
    (input_data, labels) = create_labeled_dataset(0, 10)
    model = train_model(2, 11, input_data, labels, 1250, 4)
    # test_loss, test_acc = model.evaluate(input_data, labels)
    # print(f'Test accuracy: {test_acc}')
    cur_string = ''
    for (layer_index, layer) in enumerate(model.layers):
        #g=layer.get_config()
        (weights, biases) = layer.get_weights()
        for (node_index, node_weights) in enumerate(weights):
            cur_string += 'variable {bl x_net_weight_from_' + str(layer_index) + '_' + str(node_index) + ' array ' + str(len(node_weights)) + ' DEFINE REAL per_index '
            for node_weight in node_weights:
                #cur_string += 'assign{result{' + str(int(node_weight * 100)) + '}}'
                cur_string += 'assign{result{' + str(node_weight) + '}}'
            cur_string += '}' + os.linesep
        cur_string += 'variable {bl x_net_bias_from_' + str(layer_index) + ' array ' + str(len(biases)) + ' DEFINE REAL per_index '
        for bias_weight in biases:
            #cur_string += 'assign{result{' + str(int(bias_weight * 100)) + '}}'
            cur_string += 'assign{result{' + str(bias_weight) + '}}'
        cur_string += '}' + os.linesep
    structure = [2, 10, 10, 10, 10, 11]
    previous_structure = None
    for (layer_index, cur_structure) in enumerate(structure):
        if previous_structure is None:
            for node in range(cur_structure):
                cur_string += 'variable {bl x_net_node_0_' + str(node) + ' DEFINE REAL assign{result{' + ('dest_x' if node == 0 else 'prev_dest_x') + '}}}' + os.linesep
        else:
            for node in range(cur_structure):
                cur_string += 'variable {bl x_net_node_' + str(layer_index) + '_' + str(node) + ' DEFINE REAL assign{result{' + ('(max, ' if layer_index < len(structure) - 1 else '') + '(add, '
                for prev_node in range(previous_structure):
                    cur_string += '(mult, x_net_node_' + str(layer_index - 1) + '_' + str(prev_node) + ', (index, x_net_weight_from_' + str(layer_index - 1) + '_' + str(prev_node) + ', ' + str(node) + ')),'
                cur_string += '(index, x_net_bias_from_' + str(layer_index - 1) + ', ' + str(node) + '))' + (', 0)' if layer_index < len(structure) - 1 else '') + '}}}' + os.linesep
        previous_structure = cur_structure
    cur_string +='variable {bl x_net_output_max DEFINE REAL assign{result{' + recursive_max(previous_structure - 1, layer_index) + '}}}' + os.linesep
    cur_string += (
        'variable {bl x_net_output DEFINE REAL assign{'
        + ''.join(('case{(eq, x_net_output_max, x_net_node_' + str(layer_index) + '_' + str(cur_node) + ')}result{' + str(cur_node) + '}') for cur_node in range(previous_structure))
        + 'result{-1}'
        + '}}'
    ) + os.linesep
    with open('./x_net_weights', 'w', encoding = 'utf-8') as write_file:
        write_file.write(cur_string)
idk()
