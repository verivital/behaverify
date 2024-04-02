'''
Created by Preston
'''
#
# Dataset
#
input_path = '../filled_obs/inputs_19_15_96_0.py'
target_path = "../filled_obs/targets_19_15_96_0.py"
batch_size = 2**10
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 128
hidden_count = 3
layer_sizes = [40, 32, 24]
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 2000
log_freq = 1
#
# saving
#
save_path = "../filled_obs/"
save_name = "19_15_96_0__128_3"
