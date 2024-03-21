'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputs_256_0_49_2.py'
target_path = "../ignore/targets_256_0_49_2.py"
batch_size = 4096 # 1024 for bigger stuff is reasonable.
#
# Model
#
input_size = 4
hidden_size = 128
hidden_count = 3
output_size = 5
#
# training
#
lr = 0.01
num_epochs = 4096
log_freq = 1
#
# saving
#
save_path = "../ignore"
save_name = "256_0_49_2__128_3"
