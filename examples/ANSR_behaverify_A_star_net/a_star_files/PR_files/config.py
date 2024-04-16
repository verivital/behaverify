'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputsSmallsFilled_15_15_61_1.py'
target_path = '../ignore/targetsSmallsFilled_15_15_61_1.py'
batch_size = 2**10
shuffle = True
#
# Model
#
input_size = 4
all_same = False
hidden_size = 128
hidden_count = 2
layer_sizes = [16, 8, 4]
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
save_name = '15_15_61_1__16_8_4'
