"""
This is the file, where the model gets defined, trained, evaluated and saved
"""

# pylint: disable=C0103, C0325, E0401, E0611, E1101, E1102, R0903

import time

import matplotlib.pyplot as plt  # type: ignore
import torch  # type: ignore
from torch import nn, save  # type: ignore
from torch.nn import functional as F  # type: ignore
from torch.utils.data import DataLoader  # type: ignore
from torchvision import datasets, transforms  # type: ignore

device = torch.device("mps")

number_epochs = 150
batch_size = 4
learning_rate = 0.001

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])

train_dataset = datasets.CIFAR10(root="./data", download=True, train=True, transform=transform)
test_dataset = datasets.CIFAR10(root="./data", download=True, train=False, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

classes = ("plane", "car", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck")

############# Define the Convolutional Neural Network #############
class ConvolutionalNetwork(nn.Module):
    """the definition of the network"""
    def __init__(self) -> None:
        """
        input shape of the image (32, 32, 3)
        input shape of the batch [4, 3, 32, 32]

        feature learning:
            after convolution_1 + relu [4, 6, 28, 28] ->
                    The image is smaller because the filter of the
                    convolutional layer doesn't fit in the corners
                formula: (input_width - filter_size + 2 * padding)/stride + 1
                calculation: 32x32 input, 5x5 filter, padding=0, stride=1 -> output image is 28x28
            after pooling layer [4, 6, 14, 14] ->
                    2x2 pooling layer reduces the image by a factor of 2
            after convolution_2 + relu [4, 16, 10, 10]
            after pooling layer [4, 16, 5, 5]
        classification:
            flatten -> 3D Tensor to 1D Tensor -> first linear layer input:
            16*5*5 because the output of the last pooling layer is
            16, 5, 5 (4 is the image batch size)
        """
        super(ConvolutionalNetwork, self).__init__()
        self.convolution_1 = nn.Conv2d(in_channels=3,out_channels=6,kernel_size=5)
        self.pool = nn.MaxPool2d(kernel_size=2,stride=2)
        self.convolution_2 = nn.Conv2d(in_channels=6,out_channels=16,kernel_size=5)
        self.fully_connected_layer_1 = nn.Linear(in_features=(16*5*5), out_features=120)
        self.fully_connected_layer_2 = nn.Linear(in_features=120, out_features=84)
        self.fully_connected_layer_3 = nn.Linear(in_features=84, out_features=10)

    def forward(self, x):
        """forward propagation"""
        x = self.pool(F.relu(self.convolution_1(x)))
        x = self.pool(F.relu(self.convolution_2(x)))
        x = x.view(-1, 16*5*5) # Tensor flatten
        x = F.relu(self.fully_connected_layer_1(x))
        x = F.relu(self.fully_connected_layer_2(x))
        x = self.fully_connected_layer_3(x) # no act fun -> Softmax included in CrossEntropyLoss
        return x


############# Model training #############
model = ConvolutionalNetwork().to(device=device) # load the model on the gpu
criterion = nn.CrossEntropyLoss() # Loss for multi class classification
optimizer = torch.optim.SGD(
    model.parameters(), lr=learning_rate
    ) # stochastic gradient descent optimizes the model parameters with the defined learning rate

n_total_steps = len(train_loader)
with open(
    f'src/1_machine_learning_algorithm/training_cycle_1_epoch-{number_epochs}.txt',
    'w',
    encoding="utf-8") as training_documentation:
    loss_list: list = [[], len(train_loader), [], [], [], []]
    # 2 loss 3 time 4 epoch_loss 5 epoch_mean_loss_of_all
    for epoch in range(number_epochs):
        start_time = time.time()
        loss_list[0].append(epoch + 1)
        iteration_list = []
        iteration_list_time = []
        iteration_mean_list = []
        for iteration, (images, labels) in enumerate(train_loader):
            model_parameters = model.parameters()
            # origin shape: [4, 3, 32, 32] = 4, 3, 1024
            # input layer 3 input channels, 6 output channels, 5 kernel size
            images = images.to(device) # for gpu training
            labels = labels.to(device) # for gpu training

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimze
            optimizer.zero_grad() # empty the gradients
            loss.backward()
            optimizer.step()

            if (iteration+1) % 100 == 0:
                iteration_list.append(round(loss.item(),3))
                iteration_list_time.append(iteration + 1)

            if (iteration+1) % 2500 == 0:
                text_defined = (
                f"Epoch: [{epoch+1}/{number_epochs}], "
                f"Step [{iteration+1}/{n_total_steps}], "
                f"Loss: {loss.item():.4f}")
                print(text_defined)
                training_documentation.write(text_defined)
                training_documentation.write('\n')

            if (iteration+1) % 12500 == 0:
                text_defined = f"###### Epoch {epoch + 1}: {loss.item()} ######"
                print(text_defined)
                loss_list[4].append(loss.item())
                training_documentation.write(text_defined)
                training_documentation.write('\n')

            iteration_mean_list.append(loss.item())

        mean_loss = sum(iteration_mean_list)/len(iteration_mean_list)
        text_defined = f"###### Epoch {epoch + 1} mean: {mean_loss} ######"
        print(text_defined)
        training_documentation.write(text_defined)
        training_documentation.write('\n')


        loss_list[5].append(mean_loss)
        loss_list[2].append(iteration_list)
        loss_list[3].append(iteration_list_time)
        end_time = time.time() - start_time
        text_defined = f"----- time - epoch {epoch + 1} needed {end_time} -----"
        print(text_defined)
        training_documentation.write(text_defined)
        training_documentation.write('\n')

    finished_statement = (
        f"Finished Training | total_epochs: {number_epochs}, "
        f"length of train_loader: {len(train_loader)}")
    print(finished_statement)
    training_documentation.write(finished_statement)
    training_documentation.write('\n')
    training_documentation.write("###########################")
    training_documentation.write('\n')

for iteration, list_element in enumerate(loss_list[2]):
    plt.plot(loss_list[3][iteration], loss_list[2][iteration], label = f"iteration_{iteration + 1}")

plt.xlabel("iteration")
plt.ylabel("loss")
plt.legend()
plt.savefig(f"src/1_machine_learning_algorithm/loss_function_iterations_epoch-{number_epochs}.png")
plt.show()

plt.plot(loss_list[0], loss_list[4])
plt.xlabel("epoch")
plt.ylabel("loss")
plt.savefig(f"src/1_machine_learning_algorithm/loss_function_epochs_epoch-{number_epochs}.png")
plt.show()

plt.plot(loss_list[0], loss_list[5])
plt.xlabel("epoch")
plt.ylabel("loss_mean")
plt.savefig(f"src/1_machine_learning_algorithm/loss_function_epochs_mean_epoch-{number_epochs}.png")
plt.show()

############# Model evaluation #############
with open(
    f'src/1_machine_learning_algorithm/training_cycle_1_epoch-{number_epochs}.txt',
    'a',
    encoding="utf-8") as training_documentation:
    with torch.no_grad(): # because we don't need backwards propagation and gradient calculations
        accuracy_statement = "###### start accuracy ######"
        print(accuracy_statement)
        training_documentation.write(accuracy_statement)
        training_documentation.write('\n')
        n_correct = 0
        n_samples = 0
        n_class_correct = [0 for i in range(10)]
        n_class_samples = [0 for i in range(10)]
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)

            # max returns (value, index)
            _, predicted = torch.max(outputs, 1)
            n_samples += labels.size(0)
            n_correct += (predicted == labels).sum().item()

            for i in range(batch_size):
                label = labels[i]
                pred = predicted[i]
                if (label == pred):
                    n_class_correct[label] += 1
                n_class_samples[label] += 1

        accuracy = 100.0 * n_correct / n_samples
        accuracy_statement = f"Accuracy of the network: {accuracy} %"
        print(accuracy_statement)
        training_documentation.write(accuracy_statement)
        training_documentation.write('\n')

        for i in range(10):
            accuracy = 100.0 * n_class_correct[i] / n_class_samples[i]
            accuracy_statement = f"Accuracy of {classes[i]}: {accuracy} %"
            print(accuracy_statement)
            training_documentation.write(accuracy_statement)
            training_documentation.write('\n')

############# Model saving #############
with open(
    f'src/1_machine_learning_algorithm/cnn_model_cifar10_epochs-{number_epochs}_vs1.pt',
    'wb') as model_saving:
    save(model.state_dict(), model_saving)
