'''
Created by Preston
Overnight fixes (2026-07-02):
  - `numbers` points at the current city-map data. NOTE: for data produced by
    TAYLOR_script.sh with fill_holes=1 the id includes the `Filled_` prefix
    (files are inputsFilled_<id>.py); the 2025 run was abandoned with config
    still pointing at the old map.
  - new termination knobs: `target_accuracy` (stop when train accuracy reaches
    this; the old `accuracy == 1.0` exit is unreachable on real maps) and
    `plateau_patience` (stop after this many evaluations without improvement;
    set to None to disable).
  - model capacity scaled up for the city maps: the NEUS-paper 7x7 map needed
    widths up to 5000 to memorize 2401 samples; 200x2 plateaus ~0.91 on the
    25x25 map (390,625 samples) and ~0.72 on the 50x50 map (6,250,000 samples).
'''
# #
# # Dataset
# #
numbers = 'Filled_24_80_61_2'  # 25x25 city map (block_size 40, fly_at 80)
# numbers = 'Filled_49_40_151_9'  # 50x50 city map (block_size 20, fly_at 40)

# input_path = '../scaling_scatter/inputsSmalls_' + numbers + '.py'
# target_path = '../scaling_scatter/targetsSmalls_' + numbers + '.py'
input_path = '../ignore/inputs' + numbers + '.py'
target_path = '../ignore/targets' + numbers + '.py'
batch_size = 2**14  # smaller batches = more optimizer steps per epoch; data is GPU-resident so this stays fast
shuffle = True
#
# Model
#
input_size = 4
all_same = True
hidden_size = 2048
hidden_count = 2
layer_sizes = [32, 8, 4]
output_size = 5
#
# training
#
lr = 0.001
num_epochs = 1500
log_freq = 10           # evaluate/checkpoint/log every this many epochs
target_accuracy = 0.999  # stop when train accuracy reaches this (was: == 1.0, unreachable)
plateau_patience = 30    # stop after this many evaluations without improvement (None to disable)
lr_gamma = 0.9985        # exponential lr decay per epoch (None to disable)
lr_min = 0.00005         # lr floor when decaying
#
# saving
#
save_path = '../ignore'
save_name = numbers + '__' + ((str(hidden_size) + '_' + str(hidden_count)) if all_same else '_'.join([str(x) for x in layer_sizes]))
