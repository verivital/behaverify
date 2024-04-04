'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputsSmallsFilled_15_15_61_0.py'
target_path = '../ignore/targetsSmallsFilled_15_15_61_0.py'
batch_size = 2**8
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 512
hidden_count = 1
layer_sizes = [40, 32, 24]
output_size = 5
#
# training
#
lr = 0.005
num_epochs = 2000
log_freq = 1
#
# saving
#
save_path = '../ignore'
save_name = 'SmallsFilled15_15_61_1__512_1'
