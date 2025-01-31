import onnx
from onnx import helper, numpy_helper
from onnx import AttributeProto, TensorProto, GraphProto
import onnxruntime
import numpy


# The protobuf definition can be found here:
# https://github.com/onnx/onnx/blob/main/onnx/onnx.proto

# Create one input (ValueInfoProto)
my_inputs = helper.make_tensor_value_info("my_inputs", TensorProto.FLOAT, [1, 2])
weights = numpy_helper.from_array(numpy.array([[1.75, 1.5], [1.375, -.75]], dtype = numpy.float32), name = 'weights')
biases = numpy_helper.from_array(numpy.array([-0.125, 0.25], dtype = numpy.float32), name = 'biases')
my_outputs = helper.make_tensor_value_info("my_outputs", TensorProto.FLOAT, [1, 2])

gemm = helper.make_node('Gemm', ['my_inputs', 'weights', 'biases'], ['gemm_out'])
relu = helper.make_node('Relu', ['gemm_out'], ['my_outputs'])
#argmax = helper.make_node("ArgMax", ["relu_out"], ["my_outputs"], axis=1)
###########

# Create the graph (GraphProto)
graph_def = helper.make_graph(
    [gemm, relu],        # nodes
    "test-model",      # name
    [my_inputs],  # inputs
    [my_outputs],               # outputs
    [weights, biases]
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
