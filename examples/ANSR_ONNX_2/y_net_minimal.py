import onnx
from onnx import helper, numpy_helper
from onnx import AttributeProto, TensorProto, GraphProto
import onnxruntime
import numpy


# The protobuf definition can be found here:
# https://github.com/onnx/onnx/blob/main/onnx/onnx.proto

# Create one input (ValueInfoProto)
my_inputs = helper.make_tensor_value_info("my_inputs", TensorProto.FLOAT, [1, 2])

biases_0 = numpy_helper.from_array(numpy.array([0, 0], dtype = numpy.float32), name = 'biases_0')
biases_out = numpy_helper.from_array(numpy.array([0], dtype = numpy.float32), name = 'biases_out')

weights_0 = numpy_helper.from_array(numpy.array([[1, -1], [-1, 1]], dtype = numpy.float32), name = 'weights_0')
weights_out = numpy_helper.from_array(numpy.array([[1], [1]], dtype = numpy.float32), name = 'weights_out')

my_outputs = helper.make_tensor_value_info("my_outputs", AttributeProto.FLOAT, [1, 1])


# mat_mul_0 = helper.make_node(
#     "MatMul",                  # name
#     ["my_inputs", "weights_0"], # inputs
#     ["my_inputs_1a"]                  # outputs
# )

# add_0 = helper.make_node(
#     "Add",                  # name
#     ["my_inputs_1a", "biases_0"], # inputs
#     ["my_inputs_1b"]                  # outputs
# )
gemm_0 = helper.make_node(
    'Gemm',
    ['my_inputs', 'weights_0', 'biases_0'],
    ['my_inputs_1b']
)

relu_0 = helper.make_node(
    'Relu',
    ['my_inputs_1b'],
    ['my_inputs_1']
)
###########
# mat_mul_out = helper.make_node('MatMul', ['my_inputs_1', 'weights_out'], ['my_outputs_a'])
# add_out = helper.make_node('Add', ['my_outputs_a', 'biases_out'], ['my_outputs_b'])
gemm_out = helper.make_node('Gemm', ['my_inputs_1', 'weights_out', 'biases_out'], ['my_outputs_b'])
relu_out = helper.make_node('Relu', ['my_outputs_b'], ['my_outputs'])
###########

# Create the graph (GraphProto)
graph_def = helper.make_graph(
    [gemm_0, relu_0, gemm_out, relu_out],        # nodes
    "test-model",      # name
    [my_inputs],  # inputs
    [my_outputs],               # outputs
    [weights_0, biases_0, weights_out, biases_out]
)

# Create the model (ModelProto)
onnx_model = helper.make_model(graph_def, producer_name="Serena")
converted_onnx_model = onnx.version_converter.convert_version(onnx_model, 19)


onnx.checker.check_model(converted_onnx_model)
onnx.save_model(converted_onnx_model, 'y_net.onnx')

session = onnxruntime.InferenceSession('./y_net.onnx')
x_min = 0
x_max = 3
x_mid = (x_min + x_max) / 2
for dx in range(x_min, x_max + 1):
    print_string = ''
    for px in range(x_min, x_max + 1):
        dx_true = int(dx > x_mid)
        px_true = int(px > x_mid)
        print_string += '|' + str(session.run(None, {'my_inputs' : [[dx_true, px_true]]})[0][0][0])
    print(print_string)
