'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputs_39_2_0.py'
target_path = '../ignore/targets_39_2_0.py'
batch_size = 2**10
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 128
hidden_count = 1
layer_sizes = [40, 32, 24]
output_size = 5
#
# training
#
lr = 0.01
num_epochs = 20000
log_freq = 1
#
# saving
#
save_path = '../ignore'
save_name = '39_2_0__128_1'
