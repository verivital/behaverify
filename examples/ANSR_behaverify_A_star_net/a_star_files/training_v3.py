import sys
import importlib.util
import torch
import torch.nn as nn
import torch.optim as optim
import random


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
hidden_size_arg = int(sys.argv[5])
hidden_count_arg = int(sys.argv[6])
batches = max(int(sys.argv[7]), 1)
print_rate = int(sys.argv[8]) if len(sys.argv) > 8 else 50
save_rate = int(sys.argv[9]) if len(sys.argv) > 9 else 50

print('loading inputs')
inputs = [[] for _ in range(batches)]
index = 0
with open(input_path, 'r', encoding = 'utf-8') as input_file:
    for line in input_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        inputs[index % batches].append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 1000 == 0:
            print('reading input: ' + str(index))
        index = index + 1

print('loading targets')
targets = [[] for _ in range(batches)]
index = 0
with open(target_path, 'r', encoding = 'utf-8') as target_file:
    for line in target_file.readlines():
        if ',' not in line:
            continue
        line = line.split(']', 1)[0].replace('[', '')
        targets[index % batches].append([float(line_part.strip()) for line_part in line.split(',')])
        if index % 1000 == 0:
            print('reading target: ' + str(index))
        index = index + 1

print('converting')
inputs = [torch.tensor(sub_input) for sub_input in inputs]
targets = [torch.tensor(sub_target) for sub_target in targets]


print('making network')
# Instantiate the model
#model = NeuralNetwork(input_size=4, hidden_size = 40, hidden_count = 40, output_size=5)
model = NeuralNetwork(input_size=4, hidden_size = hidden_size_arg, hidden_count = hidden_count_arg, output_size=5)

# Define loss function and optimizer
criterion = nn.MSELoss()
#optimizer = optim.SGD(model.parameters(), lr=0.01)
optimizer = optim.SGD(model.parameters(), lr=1)

print('starting training')
# Training loop
for epoch in range(num_epochs):
    # Forward pass
    batch = random.randrange(0, batches)
    # batch = epoch % batches ## for the non-random version
    outputs = model(inputs[batch])
    loss = criterion(outputs, targets[batch])

    # Calculate accuracy
    predicted_labels = torch.argmax(outputs, dim=1)
    true_labels = torch.argmax(targets[batch], dim=1)
    accuracy = torch.sum(predicted_labels == true_labels).item() / true_labels.size(0)
    if accuracy > .999:
        print(f'Epoch [{epoch}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}')
        break

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch) % print_rate == 0:
        print(f'Epoch [{epoch}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.4f}')

    if (epoch) % save_rate == 0:
        torch.save(model.state_dict(), output_path)

# Optionally, save the trained model
torch.save(model.state_dict(), output_path)
