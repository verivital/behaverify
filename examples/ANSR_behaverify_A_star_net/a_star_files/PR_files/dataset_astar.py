'''
Created by Preston
'''
import torch
from torch.utils.data import Dataset
import importlib.util

class AStarDataset(Dataset):
    def __init__(self, input_path, target_path):
        """
        Dataset for Astar inputs and targets.
        """
        #
        # Read inputs
        #
        spec = importlib.util.spec_from_file_location("data_module", input_path)
        data_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data_module)
        self.inputs = data_module.inputs
        #
        # Read targets
        #
        spec = importlib.util.spec_from_file_location("data_module", target_path)
        data_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data_module)
        self.targets = data_module.targets

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
