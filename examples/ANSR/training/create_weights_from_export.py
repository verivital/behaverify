import numpy
import os

def save_model_int():
    cur_string = ''
    str_weights = {}
    str_biases = {}
    for (layer_index) in range(5):
        weights = numpy.load('./exported_vals/w_' + str(layer_index))
        for (target_node_index, node_weights) in enumerate(weights):
            for (source_node_index, node_weight) in enumerate(node_weights):
                str_weights[(layer_index, source_node_index, target_node_index)] = str(node_weight)
        biases = numpy.load('./exported_vals/b_' + str(layer_index))
        for (target_node_index, bias_weight) in enumerate(biases):
            str_biases[(layer_index, target_node_index)] = str(bias_weight)
    structure = [2, 10, 10, 10, 10, 11]
    previous_structure = None
    print(str_weights)
    for (layer_index, cur_structure) in enumerate(structure):
        if previous_structure is None:
            for node in range(cur_structure):
                cur_string += 'variable {bl x_net_node_0_' + str(node) + ' DEFINE INT assign{result{' + ('dest_x' if node == 0 else 'prev_dest_x') + '}}}' + os.linesep
        else:
            for node in range(cur_structure):
                cur_string += 'variable {bl x_net_node_' + str(layer_index) + '_' + str(node) + ' DEFINE INT assign{result{' + ('(max, ' if layer_index < len(structure) - 1 else '') + '(add, '
                for prev_node in range(previous_structure):
                    cur_string += '(mult, x_net_node_' + str(layer_index - 1) + '_' + str(prev_node) + ', ' + str_weights[((layer_index - 1), prev_node, node)] + '),'
                    # cur_string += '(mult, x_net_node_' + str(layer_index - 1) + '_' + str(prev_node) + ', (index, x_net_weight_from_' + str(layer_index - 1) + '_' + str(prev_node) + ', ' + str(node) + ')),'
                cur_string += str_biases[((layer_index - 1), node)] + ')' + (', 0)' if layer_index < len(structure) - 1 else '') + '}}}' + os.linesep
                # cur_string += '(index, x_net_bias_from_' + str(layer_index - 1) + ', ' + str(node) + '))' + (', 0)' if layer_index < len(structure) - 1 else '') + '}}}' + os.linesep
        previous_structure = cur_structure
    #cur_string +='variable {bl x_net_output_max DEFINE REAL assign{result{' + recursive_max(previous_structure - 1, layer_index) + '}}}' + os.linesep
    cur_string +='variable {bl x_net_output_max DEFINE INT assign{result{(max, ' + ', '.join(('x_net_node_' + str(layer_index) + '_' + str(node)) for node in range(previous_structure)) + ')}}}' + os.linesep
    cur_string += (
        'variable {bl x_net_output DEFINE INT assign{'
        + ''.join(('case{(eq, x_net_output_max, x_net_node_' + str(layer_index) + '_' + str(cur_node) + ')}result{' + str(cur_node) + '}') for cur_node in range(previous_structure))
        + 'result{-1}'
        + '}}'
    ) + os.linesep
    with open('./x_net_weights_int', 'w', encoding = 'utf-8') as write_file:
        write_file.write(cur_string)

save_model_int()
