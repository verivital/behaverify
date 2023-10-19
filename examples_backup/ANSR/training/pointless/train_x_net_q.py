import torch
#import torch.nn as nn
#import torch.optim as optim

#import random
import numpy

# Define a neural network with the specified architecture
class CustomNet(torch.nn.Module):
    def __init__(self):
        super(CustomNet, self).__init__()
        self.relu=torch.nn.ReLU()
        self.softmax=torch.nn.Softmax(1)
        self.fc1 = torch.nn.Linear(2, 10)
        self.fc2 = torch.nn.Linear(10, 10)
        self.fc3 = torch.nn.Linear(10, 10)
        self.fc4 = torch.nn.Linear(10, 10)
        self.fc5 = torch.nn.Linear(10, 11)  # Output layer with 11 neurons (hardmax)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.relu(self.fc4(x))
        #x = self.fc5(x)
        x = self.softmax(self.fc5(x))
        return x


# we assume [x1, x0] means current location, previous destination.
def convert_to_array(label, x_min, x_max):
    array_label = [0] * (x_max + 1 - x_min)
    array_label[label] = 1
    return array_label

def create_labeled_dataset(x_min, x_max):
    x_mid = (x_max + x_min)/2
    input_data = [[x1, x2] for x1 in range(x_min, x_max + 1) for x2 in range(x_min, x_max + 1)]
    #labels = list(map(lambda input_vals: ((x_min if input_vals[1] >= x_mid else x_max) if input_vals[0] == input_vals[1] else input_vals[0]), input_data))
    labels = list(map(lambda input_vals: convert_to_array(((x_min if input_vals[1] >= x_mid else x_max) if input_vals[0] == input_vals[1] else input_vals[0]), x_min, x_max), input_data))
    return (numpy.array(input_data), numpy.array(labels))

# Function to calculate accuracy
def calculate_accuracy(outputs, labels):
    correct = 0
    total = 0
    for index in range(len(labels)):
        total = total + 1
        # max_loc = -1
        # max_val = -1
        # for index2 in range(len(outputs[index])):
        #     if outputs[in
        correct = correct + (1 if torch.argmax(outputs[index]) == torch.argmax(labels[index]) else 0)
    # _, predicted = torch.argmax(outputs, 1)
    # correct = (predicted == labels).sum().item()
    # total = labels.size(0)
    return correct / total

# Generate random data
def my_training():
    (input_data, labels) = create_labeled_dataset(0, 10)
    # Convert data and labels to PyTorch tensors
    # converted_input_data = torch.Tensor(input_data, dtype=torch.int8)
    # converted_labels = torch.Tensor(labels, dtype=torch.int8)
    converted_input_data = torch.Tensor(input_data)
    converted_labels = torch.Tensor(labels)

    # Create a DataLoader for the dataset
    dataset = torch.utils.data.TensorDataset(converted_input_data, converted_labels)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=True)

    # Create an instance of the model
    net = CustomNet()

    # Define loss function and optimizer
    criterion = torch.nn.CrossEntropyLoss()
    # criterion = torch.nn.L1Loss()
    #optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    optimizer = torch.optim.Adam(net.parameters())

    # Train the model
    for epoch in range(1000):  # You can adjust the number of epochs
        running_loss = 0.0
        running_accuracy = 0.0
        for i, data in enumerate(dataloader, 0):
            inputs, labels = data

            # Zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = net(inputs)
            loss = criterion(outputs, labels)

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            running_accuracy += calculate_accuracy(outputs, labels)

        #print(f"Epoch {epoch+1}, Loss: {running_loss / len(dataloader)}")
        print(f"Epoch {epoch+1}, Accuracy: {running_accuracy / len(dataloader)}")

    # Save the trained model
    outputs = net(converted_input_data)
    print(converted_input_data[0])
    print(converted_labels[0])
    print(outputs[0])
    print(sum(outputs[0]))
    torch.save(net.state_dict(), 'custom_net.pth')

my_training()
