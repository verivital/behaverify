'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputs_119_0_49_2.py'
target_path = "../ignore/targets_119_0_49_2.py"
batch_size = 2**5
shuffle = False
#
# Model
#
input_size = 4
all_same = True
hidden_size = 8192
hidden_count = 1
layer_sizes = [40, 32, 24]
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 10000
log_freq = 1
#
# saving
#
save_path = "../ignore"
save_name = "119_0_49_2__8192_1"
