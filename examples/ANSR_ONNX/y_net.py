import onnx
from onnx import helper, numpy_helper
from onnx import AttributeProto, TensorProto, GraphProto
import onnxruntime
import numpy


# The protobuf definition can be found here:
# https://github.com/onnx/onnx/blob/main/onnx/onnx.proto

y_min = 0
y_max = 8
y_mid = (y_min + y_max) / 2
delta_y = 2

# Create one input (ValueInfoProto)
my_inputs = helper.make_tensor_value_info("my_inputs", TensorProto.FLOAT, [1, 3])

biases_0 = numpy_helper.from_array(numpy.array([0, 0, 0, 0, 0], dtype = numpy.float32), name = 'biases_0')
biases_1 = numpy_helper.from_array(numpy.array([0, 0, 1, 0, 0], dtype = numpy.float32), name = 'biases_1')
biases_2 = numpy_helper.from_array(numpy.array([0, -1, 0, -1, 0], dtype = numpy.float32), name = 'biases_2')
biases_out = numpy_helper.from_array(numpy.array([0], dtype = numpy.float32), name = 'biases_out')

weights_0 = numpy_helper.from_array(numpy.array([[1, 1, -1, 0, 0], [0, -1, 1, 0, 0], [0, 0, 0, 1, -1]], dtype = numpy.float32), name = 'weights_0')
weights_1 = numpy_helper.from_array(numpy.array([[1, 0, 0, 0, 0], [0, 0, -1, 0, 0], [0, 0, -1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype = numpy.float32), name = 'weights_1')
weights_2 = numpy_helper.from_array(numpy.array([[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0]], dtype = numpy.float32), name = 'weights_2')
weights_out = numpy_helper.from_array(numpy.array([[1], [delta_y], [0], [-1 * delta_y], [0]], dtype = numpy.float32), name = 'weights_out')

my_outputs = helper.make_tensor_value_info("my_outputs", AttributeProto.FLOAT, [1, 1])


mat_mul_0 = helper.make_node(
    "MatMul",                  # name
    ["my_inputs", "weights_0"], # inputs
    ["my_inputs_1a"]                  # outputs
)

add_0 = helper.make_node(
    "Add",                  # name
    ["my_inputs_1a", "biases_0"], # inputs
    ["my_inputs_1b"]                  # outputs
)

relu_0 = helper.make_node(
    'Relu',
    ['my_inputs_1b'],
    ['my_inputs_1']
)

mat_mul_1 = helper.make_node('MatMul', ['my_inputs_1', 'weights_1'], ['my_inputs_2a'])
add_1 = helper.make_node('Add', ['my_inputs_2a', 'biases_1'], ['my_inputs_2b'])
relu_1 = helper.make_node('Relu', ['my_inputs_2b'], ['my_inputs_2'])
###########
mat_mul_2 = helper.make_node('MatMul', ['my_inputs_2', 'weights_2'], ['my_inputs_3a'])
add_2 = helper.make_node('Add', ['my_inputs_3a', 'biases_2'], ['my_inputs_3b'])
relu_2 = helper.make_node('Relu', ['my_inputs_3b'], ['my_inputs_3'])
###########
mat_mul_out = helper.make_node('MatMul', ['my_inputs_3', 'weights_out'], ['my_outputs_a'])
add_out = helper.make_node('Add', ['my_outputs_a', 'biases_out'], ['my_outputs_b'])
relu_out = helper.make_node('Relu', ['my_outputs_b'], ['my_outputs'])
###########

# Create the graph (GraphProto)
graph_def = helper.make_graph(
    [mat_mul_0, add_0, relu_0, mat_mul_1, add_1, relu_1, mat_mul_2, add_2, relu_2, mat_mul_out, add_out, relu_out],        # nodes
    "test-model",      # name
    [my_inputs],  # inputs
    [my_outputs],               # outputs
    [weights_0, biases_0, weights_1, biases_1, weights_2, biases_2, weights_out, biases_out]
)

# Create the model (ModelProto)
onnx_model = helper.make_model(graph_def, producer_name="Serena")
converted_onnx_model = onnx.version_converter.convert_version(onnx_model, 19)


onnx.checker.check_model(converted_onnx_model)
onnx.save_model(converted_onnx_model, 'y_net.onnx')

session = onnxruntime.InferenceSession('/home/serene/temp/y_net.onnx')
print('direction, up')
for dx in range(y_min, y_max + 1):
    print_string = ''
    for px in range(y_min, y_max + 1):
        print_string += '|' + str(session.run(None, {'my_inputs' : [[dx, px, 1]]})[0][0][0])
    print(print_string)
print('direction, down')
for dx in range(y_min, y_max + 1):
    print_string = ''
    for px in range(y_min, y_max + 1):
        print_string += '|' + str(session.run(None, {'my_inputs' : [[dx, px, -1]]})[0][0][0])
    print(print_string)
#results = session.run(None, {'my_inputs' : [[10, 9]]})
#print(results[0][0][0])
#print(results)
