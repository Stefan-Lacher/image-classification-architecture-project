# Machine Learning Algorithm folder

This is the description for the folder Machine Learning Algorithm:

## Data
For the creation of the machine learning algorithm, 32x32 RGB images of planes, cars, birds, cats, deer, dogs, frogs, horses, ships and trucks were treated. The database is called CIFAR-10 and contains 60000, 6000 per class, images.

## Architecture




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


