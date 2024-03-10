import sys
import importlib.util
import torch
import torch.nn as nn
import torch.optim as optim


# Define the neural network architecture
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, hidden_count, output_size):
        super(NeuralNetwork, self).__init__()
        self.hidden_layers = nn.ModuleList()
        self.hidden_layers.append(nn.Linear(input_size, hidden_size))
        for _ in range(hidden_count):  # 30 hidden layers
            self.hidden_layers.append(nn.Linear(hidden_size, hidden_size))
        self.output_layer = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        for layer in self.hidden_layers:
            x = self.relu(layer(x))
        x = self.output_layer(x)
        return x

# Define training data
num_epochs = int(sys.argv[1])
input_path = sys.argv[2]
target_path = sys.argv[3]
output_path = sys.argv[4]

input_spec = importlib.util.spec_from_file_location("input_module", input_path)
input_module = importlib.util.module_from_spec(input_spec)
input_spec.loader.exec_module(input_module)

target_spec = importlib.util.spec_from_file_location("target_module", target_path)
target_module = importlib.util.module_from_spec(target_spec)
target_spec.loader.exec_module(target_module)

inputs = torch.tensor(input_module.inputs)
targets = torch.tensor(target_module.targets)

# Instantiate the model
#model = NeuralNetwork(input_size=4, hidden_size = 40, hidden_count = 40, output_size=5)
model = NeuralNetwork(input_size=4, hidden_size = 20, hidden_count = 10, output_size=5)

# Define loss function and optimizer
criterion = nn.MSELoss()
#optimizer = optim.SGD(model.parameters(), lr=0.01)
optimizer = optim.SGD(model.parameters(), lr=1)

# Training loop
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(inputs)
    loss = criterion(outputs, targets)

    # Calculate accuracy
    predicted_labels = torch.argmax(outputs, dim=1)
    true_labels = torch.argmax(targets, dim=1)
    accuracy = torch.sum(predicted_labels == true_labels).item() / true_labels.size(0)
    if accuracy > .999:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}')
        break

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}')

# Optionally, save the trained model
torch.save(model.state_dict(), output_path)
