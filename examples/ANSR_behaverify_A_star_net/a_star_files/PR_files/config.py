'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputs_4_0_19_3_new.py'
target_path = "../ignore/targets_4_0_19_3_new.py"
batch_size = 2**10
shuffle = False
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
lr = 0.001
num_epochs = 1000
log_freq = 1
#
# saving
#
save_path = "../ignore"
save_name = "4_0_19_3_new__512_1"
