'''
Created by Preston
'''
import torch
from torch.utils.data import Dataset
import importlib.util


def _parse_rows(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as data_file:
        for line in data_file:
            if ',' not in line:
                continue
            line = line.split(']', 1)[0].replace('[', '')
            rows.append([float(line_part.strip()) for line_part in line.split(',')])
    return rows


def load_tensors(input_path, target_path):
    """
    Parse the generated inputs/targets text files ONCE into tensors.
    Returns (inputs float32 [N, 4], targets long [N]) with one-hot targets
    converted to class indices. This replaces the per-sample DataLoader
    collation, which was the training-throughput bottleneck (see training.py).
    """
    inputs = torch.tensor(_parse_rows(input_path), dtype=torch.float32)
    targets_raw = torch.tensor(_parse_rows(target_path))
    if targets_raw.dim() > 1 and targets_raw.shape[1] > 1:
        targets = targets_raw.argmax(dim=1).type(torch.long)
    else:
        targets = targets_raw.reshape(-1).type(torch.long)
    if inputs.shape[0] == 0:
        raise RuntimeError('no training samples parsed from ' + input_path
                           + ' -- was the map degenerate (all obstacles / empty table)?')
    if inputs.shape[0] != targets.shape[0]:
        raise RuntimeError('inputs/targets length mismatch: '
                           + str(inputs.shape[0]) + ' vs ' + str(targets.shape[0]))
    return (inputs, targets)


class AStarDataset(Dataset):
    def __init__(self, input_path, target_path):
        """
        Dataset for Astar inputs and targets.
        """
        print('loading inputs')
        inputs = []
        index = 0
        with open(input_path, 'r', encoding = 'utf-8') as input_file:
            for line in input_file.readlines():
                if ',' not in line:
                    continue
                line = line.split(']', 1)[0].replace('[', '')
                inputs.append([float(line_part.strip()) for line_part in line.split(',')])
                if index % 1000 == 0:
                    print('reading input: ' + str(index))
                index = index + 1

        print('loading targets')
        targets = []
        index = 0
        with open(target_path, 'r', encoding = 'utf-8') as target_file:
            for line in target_file.readlines():
                if ',' not in line:
                    continue
                line = line.split(']', 1)[0].replace('[', '')
                targets.append([float(line_part.strip()) for line_part in line.split(',')])
                if index % 1000 == 0:
                    print('reading target: ' + str(index))
                index = index + 1

        self.inputs = inputs
        self.targets = targets
        # #
        # # Read inputs
        # #
        # spec = importlib.util.spec_from_file_location("data_module", input_path)
        # data_module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(data_module)
        # self.inputs = data_module.inputs
        # #
        # # Read targets
        # #
        # spec = importlib.util.spec_from_file_location("data_module", target_path)
        # data_module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(data_module)
        # self.targets = data_module.targets

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        #
        # Get data
        #
        input_data = torch.tensor(self.inputs[idx], dtype=torch.float32)
        #
        # Convert one-hot to a class label
        #
        if len(self.targets[idx]) > 0:
            target_data = torch.argmax(torch.tensor(self.targets[idx]), dim=-1).type(torch.long)
        else:
            # If targets are already class indices
            target_data = torch.tensor(self.targets[idx], dtype=torch.long)
        
        return input_data, target_data
