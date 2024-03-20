'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputs_3_0_7_1.py'
target_path = "../ignore/targets_3_0_7_1.py"
batch_size = 1024 # 1024 for bigger stuff is reasonable.
#
# Model
#
input_size = 4
hidden_size = 32
hidden_count = 3
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 1024
log_freq = 1
#
# saving
#
save_path = "../ignore"
save_name = "3_0_7_1__32_3"
