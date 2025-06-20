'''
Created by Preston
'''
# #
# # Dataset
# #
numbers = '24_80_61_2'

# input_path = '../scaling_scatter/inputsSmalls_' + numbers + '.py'
# target_path = '../scaling_scatter/targetsSmalls_' + numbers + '.py'
input_path = '../ignore/inputs_' + numbers + '.py'
target_path = '../ignore/targets_' + numbers + '.py'
batch_size = 2**20
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 200
hidden_count = 2
layer_sizes = [32, 8, 4]
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 100000
log_freq = 1
#
# saving
#
save_path = '../ignore'
save_name = numbers + '__' + ((str(hidden_size) + '_' + str(hidden_count)) if all_same else '_'.join([str(x) for x in layer_sizes]))


#
# Dataset
#

# num = 10

# input_path = str(num) + 'prime_inputs.py'
# target_path = str(num) + 'prime_targets.py'
# batch_size = 2**6
# shuffle = False
# #
# # Model
# #
# input_size = 1
# all_same = True
# hidden_size = 20
# hidden_count = 1
# layer_sizes = [32, 8, 4]
# output_size = 2
# #
# # training
# #
# lr = 0.001
# num_epochs = 2000
# log_freq = 1
# #
# # saving
# #
# save_path = './'
# save_name =  str(num) + 'prime__' + ((str(hidden_size) + '_' + str(hidden_count)) if all_same else '_'.join([str(x) for x in layer_sizes]))
