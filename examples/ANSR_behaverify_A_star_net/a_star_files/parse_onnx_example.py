import sys
import onnx
import numpy as np

# Load the ONNX model
#model = onnx.load("32_001.onnx")
model = onnx.load(sys.argv[1])

# Print the basic information about the model
print(onnx.helper.printable_graph(model.graph))

# Iterate through the model's nodes and print information about each node
for node in model.graph.node:
    print("Node Name:", node.name)
    print("Op Type:", node.op_type)
    print("Input(s):", node.input)
    print("Output(s):", node.output)
    print()

# Access model inputs and outputs
print("Model Inputs:", [input.name for input in model.graph.input])
print("Model Outputs:", [output.name for output in model.graph.output])

# Access model initializer (weights) and their values
print("Model Initializers:")
for init in model.graph.initializer:
    print("Name:", init.name)
    print("Shape:", init.dims)
    print("Data Type:", init.data_type)
    array = onnx.numpy_helper.to_array(init)
    print("Values:", array)
    print()
