'''
Created by Preston
'''
import sys
import time
from dataset_astar import AStarDataset
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim
import config as c
import os
import torch.onnx


class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, hidden_count, output_size):
        super(NeuralNetwork, self).__init__()
        self.hidden_layers = nn.ModuleList()
        self.hidden_layers.append(nn.Linear(input_size, hidden_size))
        for _ in range(hidden_count - 1):
            self.hidden_layers.append(nn.Linear(hidden_size, hidden_size))
        self.output_layer = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        for layer in self.hidden_layers:
            x = self.relu(layer(x))
        x = self.output_layer(x)
        return x

def test(trained_model, test_loader, device):
    """
    Test model. 
    """
    trained_model.eval()
    total_corr = 0
    total_items = 0
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = trained_model(inputs)
            predicted_classes = outputs.argmax(dim=1)
            total_corr += (predicted_classes == targets).sum().item()
            total_items += targets.size(0)
    return total_corr / total_items

def train(model, train_loader, criterion, optimizer, device):
    """
    Train model.
    """
    model.train()
    total_loss = 0
    for inputs, targets in train_loader:
        if SLEEP_MODE:
            time.sleep(.005)
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(train_loader)

def main():
    """
    Main
    """
    #
    # Check device
    #
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n\nUsing device: {device}\n\n")
    os.makedirs(c.save_path, exist_ok=True)
    #
    # Load dataset
    #
    dataset = AStarDataset(c.input_path, c.target_path)
    dataloader = DataLoader(dataset, batch_size=c.batch_size, shuffle=True)
    #
    # Setup hyperparameters
    #
    model = NeuralNetwork(c.input_size, c.hidden_size, c.hidden_count, c.output_size).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=c.lr)
    #
    # RUN
    #
    for epoch in range(c.num_epochs):
        #
        # Train
        #
        loss = train(model, dataloader, criterion, optimizer, device)
        #
        # Test
        #
        if epoch % c.log_freq == 0:
            accuracy = test(model, dataloader, device)
            print(f"[{epoch}/{c.num_epochs}] Accuracy: {accuracy:.4f} \t Loss: {loss:.4f}")
            torch.save(model, os.path.join(c.save_path, c.save_name+".pth"))
            if accuracy == 1.0:
                break

    #
    # Save the model
    #
    print("\n\n Finished Training. Saving models ..................................................")
    torch.save(model, os.path.join(c.save_path, c.save_name+".pth"))
    #
    # Convert to onnx and save --> need to fix
    #
    model.eval()
    dummy_input = torch.randn(1, c.input_size).to(device)  # Adjust the dummy input as per your model's requirement
    torch.onnx.export(model,
                      dummy_input,
                      os.path.join(c.save_path, c.save_name + ".onnx"),
                      export_params=True,
                      opset_version=11,
                      do_constant_folding=True,
                      input_names=['input'],
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'},
                                    'output': {0: 'batch_size'}})

    print("\n\n------------------------------------- Finished Training -------------------------------------------\n\n")


def resume_training():
    """
    Main
    """
    #
    # Check device
    #
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n\nUsing device: {device}\n\n")
    os.makedirs(c.save_path, exist_ok=True)
    #
    # Load dataset
    #
    dataset = AStarDataset(c.input_path, c.target_path)
    dataloader = DataLoader(dataset, batch_size=c.batch_size, shuffle=True)
    print(len(dataloader))
    #
    # Setup hyperparameters
    #
    model = torch.load(os.path.join(c.save_path, c.save_name+".pth"))
    #model = NeuralNetwork(c.input_size, c.hidden_size, c.hidden_count, c.output_size).to(device)
    #model.load_state_dict(torch.load(os.path.join(c.save_path, c.save_name+".pth")))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=c.lr)
    #
    # RUN
    #
    for epoch in range(c.num_epochs):
        #
        # Train
        #
        loss = train(model, dataloader, criterion, optimizer, device)
        #
        # Test
        #
        if epoch % c.log_freq == 0:
            accuracy = test(model, dataloader, device)
            print(f"[{epoch}/{c.num_epochs}] Accuracy: {accuracy:.4f} \t Loss: {loss:.4f}")
            torch.save(model, os.path.join(c.save_path, c.save_name+".pth"))
            if accuracy == 1.0:
                break

    #
    # Save the model
    #
    print("\n\n Finished Training. Saving models ..................................................")
    torch.save(model, os.path.join(c.save_path, c.save_name+".pth"))
    #
    # Convert to onnx and save --> need to fix
    #
    model.eval()
    dummy_input = torch.randn(1, c.input_size).to(device)  # Adjust the dummy input as per your model's requirement
    torch.onnx.export(model,
                      dummy_input,
                      os.path.join(c.save_path, c.save_name + ".onnx"),
                      export_params=True,
                      opset_version=11,
                      do_constant_folding=True,
                      input_names=['input'],
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'},
                                    'output': {0: 'batch_size'}})

    print("\n\n------------------------------------- Finished Training -------------------------------------------\n\n")
SLEEP_MODE = False
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '0':
            SLEEP_MODE = True
            main()
        elif sys.argv[1] == '1':
            resume_training()
        elif sys.argv[1] == '2':
            SLEEP_MODE = True
            resume_training()
    else:
        main()
