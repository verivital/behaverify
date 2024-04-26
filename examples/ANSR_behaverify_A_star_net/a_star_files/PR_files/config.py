'''
Created by Preston
'''
#
# Dataset
#
input_path = '../ignore/inputsSmallsFilled_49_07_560_5.py'
target_path = '../ignore/targetsSmallsFilled_49_07_560_5.py'
batch_size = 2**15
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 512
hidden_count = 2
layer_sizes = [32, 8, 4]
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 200000
log_freq = 1
#
# saving
#
save_path = '../ignore'
save_name = '49_07_560_5__512_2'
