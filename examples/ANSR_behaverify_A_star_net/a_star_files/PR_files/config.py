'''
Created by Preston
'''
# #
# # Dataset
# #
numbers = '6_18_0'

input_path = '../scaling_scatter/inputsSmalls_' + numbers + '.py'
target_path = '../scaling_scatter/targetsSmalls_' + numbers + '.py'
batch_size = 2**20
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 5000
hidden_count = 1
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
save_path = '../scaling_scatter'
save_name = numbers + '__' + ((str(hidden_size) + '_' + str(hidden_count)) if all_same else '_'.join([str(x) for x in layer_sizes]))


#
# Dataset
#

# num = 20

# input_path = str(num) + 'prime_inputs.py'
# target_path = str(num) + 'prime_targets.py'
# batch_size = 2**5
# shuffle = True
# #
# # Model
# #
# input_size = 1
# all_same = True
# hidden_size = 50
# hidden_count = 1
# layer_sizes = [32, 8, 4]
# output_size = 2
# #
# # training
# #
# lr = 0.001
# num_epochs = 200000
# log_freq = 1
# #
# # saving
# #
# save_path = './'
# save_name =  str(num) + 'prime__' + ((str(hidden_size) + '_' + str(hidden_count)) if all_same else '_'.join([str(x) for x in layer_sizes]))
