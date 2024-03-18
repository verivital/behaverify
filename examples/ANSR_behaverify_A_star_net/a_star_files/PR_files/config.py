'''
Created by Preston
'''
#
# Dataset
#
input_path = "../ignore/inputs_256_0_49_2.py"
target_path = "../ignore/targets_256_0_49_2.py"
# input_path = "../ignore/inputs_10_0_9_1.py"
# target_path = "../ignore/targets_10_0_9_1.py"
batch_size = 1024
#
# Model
#
input_size = 4
hidden_size = 32
hidden_count = 1
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 100000
log_freq = 5
#
# saving
#
save_path = "../ignore"
save_name = "256_0_49_2___32_001"
# save_name = "10_0_9_1___32_001"
