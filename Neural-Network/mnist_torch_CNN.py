import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np


def load_mnist_data_train(file_name):
    return data


def load_mnist_data_test(file_name):
    return data


data_set = load_mnist_data_train(train_file_name)
test_data = load_mnist_data_test(test_file_name)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# loop over the dataset multiple times
for epoch in range(2):

    running_loss = 0.0

    for i in range(len(data_set)):

        # create labels
        labels = torch.zeros(1, 10)
        labels[data_set[i][0]] = 1

        # create inputs
        inputs = []
        for j in range(len(data_set)-1):
            inputs.append(data_set[i][j+1])
        inputs = np.array(inputs)
        inputs.reshape((28, 28))
        inputs = torch.tensor(inputs)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        # print every 2000 mini-batches
        if i % 2000 == 1999:
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0


print('Finished Training')

correct = 0
total = 0
with torch.no_grad():
    for i in range(len(test_data)):
        # create labels
        labels = torch.zeros(1, 10)
        labels[test_data[i][0]] = 1

        # create inputs
        images = []
        for j in range(len(test_data)-1):
            images.append(test_data[i][j+1])
        images = np.array(images)
        images.reshape((28, 28))
        images = torch.tensor(images)
        # images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the 10000 test images: %d %%' % (
    100 * correct / total))
