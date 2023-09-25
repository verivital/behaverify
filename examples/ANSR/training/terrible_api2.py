import tensorflow as tf
import h5py
import numpy as np

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="tflite_model.tflite")
interpreter.allocate_tensors()

# # Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Prepare the input data
input_data = np.array([[0, 0]], dtype=np.int8)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])

# Print the prediction
print("Predicted value:", output_data)


# get details for each layer
all_layers_details = interpreter.get_tensor_details() 


f = h5py.File("mobilenet_v3_weights_infos.hdf5", "w")

for layer in all_layers_details:
     # to create a group in an hdf5 file
     grp = f.create_group(str(layer['index']))

     # to store layer's metadata in group's metadata
     grp.attrs["name"] = layer['name']
     grp.attrs["shape"] = layer['shape']
     # grp.attrs["dtype"] = all_layers_details[i]['dtype']
     grp.attrs["quantization"] = layer['quantization']

     # to store the weights in a dataset
     grp.create_dataset("weights", data=interpreter.get_tensor(layer['index']))


f.close()
