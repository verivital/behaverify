import numpy as np
import tensorflow as tf

# Generate a simple neural network model with 2 hidden layers
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(1,), dtype=tf.float32),  # Input layer with one feature
    tf.keras.layers.Dense(64, activation='relu'),         # First hidden layer with ReLU activation
    tf.keras.layers.Dense(32, activation='relu'),         # Second hidden layer with ReLU activation
    tf.keras.layers.Dense(2, activation='softmax')        # Output layer with two units (for binary classification)
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define a function to generate representative data
def representative_data_gen():
    for _ in range(1):
        # Generate random input data within the range of your model's inputs
        #input_data = np.random.randint(0, 100, size=(1, 1), dtype=np.float32)  # Modify batch_size as needed
        input_data = np.float32(np.random.randint(0, 100, size=(1, 1)))  # Modify batch_size as needed
        yield [input_data]

# Set the representative dataset in the converter
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.representative_dataset = representative_data_gen
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert the model to a TensorFlow Lite model
tflite_model = converter.convert()

# Save the TensorFlow Lite model to a file
with open("model.tflite", "wb") as f:
    f.write(tflite_model)
