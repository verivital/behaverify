import numpy as np
import tensorflow as tf

# Load the TensorFlow Lite model
tflite_model_path = 'tflite_model.tflite'  # Replace with the path to your .tflite model file
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Prepare the input data
input_data = np.array([[0, 0]], dtype=np.int8)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Print the prediction
print("Predicted value:", output_data)
