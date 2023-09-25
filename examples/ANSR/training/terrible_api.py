'''
Create interpreter, allocate tensors
'''
import os
import tensorflow as tf
import numpy
from tensorflow import keras

from keras.utils import plot_model
from graphviz import Digraph

tflite_interpreter = tf.lite.Interpreter(model_path='tflite_model.tflite')
tflite_interpreter.allocate_tensors()

'''
Check input/output details
'''
input_details = tflite_interpreter.get_input_details()
output_details = tflite_interpreter.get_output_details()

print("== Input details ==")
print("name:", input_details[0]['name'])
print("shape:", input_details[0]['shape'])
print("type:", input_details[0]['dtype'])
print("\n== Output details ==")
print("name:", output_details[0]['name'])
print("shape:", output_details[0]['shape'])
print("type:", output_details[0]['dtype'])

'''
Run prediction (optional), input_array has input's shape and dtype
'''
tflite_interpreter.set_tensor(input_details[0]['index'], [numpy.int8([0, 0])])
tflite_interpreter.invoke()
output_array = tflite_interpreter.get_tensor(output_details[0]['index'])

'''
This gives a list of dictionaries. 
'''
tensor_details = tflite_interpreter.get_tensor_details()

for dict_ in tensor_details:
    i = dict_['index']
    tensor_name = dict_['name']
    scales = dict_['quantization_parameters']['scales']
    zero_points = dict_['quantization_parameters']['zero_points']
    tensor = tflite_interpreter.tensor(i)()

    print(i, tensor_name, scales.shape, zero_points.shape, tensor.shape)
    print(zero_points)
    print(tensor_details[i])

    '''
    See note below
    '''
