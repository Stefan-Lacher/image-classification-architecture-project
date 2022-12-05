# Image analysis project

The idea behind this project is to have an image stream from which the images are coming from and the analysis of the images run in parallel and in real time. Finally, the final results must be calculated and submitted.

There are five main areas that will be covered:
1. Develop machine learning algorithm
2. Image stream
3. Image processing
4. Image analysis
5. End results calculation


## Machine Learning Algorithm
The machine learning algorithm to be developed should recognize 10 different types of fashion in images and then output a result. To implement the analysis, an Convolutional Neural Network classifier is developed using Pytorch. 

## Image stream
Here a dataset pickle of images is taken, which are saved in binary, uint8 format. In addition, a web socket stream will be built, through which the images will be transmitted at 10 frames per second. The idea behind this is to be able to start and stop a session in order to be able to calculate the number of transferred images on both sides and to be ready for the transfer on both sides. In addition, the final results should be able to be sent back.

Thus, the development points are as follows:
- Create a dataset with a specified number of images in pickle format
- Create websocket stream for image transmission with port: 6000
- Create websocket stream for session management, image transfer calculation and results submission with port: 7000

## Image processing
When processing the images, a connection to the websocket stream must be established in order to receive the images. Then these are converted from binary, uint8 format into a numpy array, adjusted in size and written to a queue.

The development points are as follows:
- Create a websocket connection in the form of a listener
- Convert the image to a numpy array
- Check and adjust size
- Create a cross-thread queue and write the image to it

## Image analysis
When analyzing the images, the first image is taken from the queue, analyzed using a machine learning algorithm and the result is written to a queue together with the image.

The development points are as follows:
- image received
- Apply machine learning algorithm
- Create a queue and write results and images to it

## End results calculation
In the last step, the results queue is used to calculate the final results. In addition, overview metrics are created. In addition, 10 example images are selected with the respective results, which should serve as a small check. Finally, it calculates how many images were received and how many of the images Stream indicates. All results are put into a transferable form and sent back.

The development points are as follows:
- Create summary metrics
- Automatically select 10 sample images and write the result into the image
- Calculate number of total images and set up comparison with image stream
- Create transferable form
- Send back results

# Basic principles

In addition to this project, there are basic principles that are adhered to.
1. PEP8 checked with pylint
2. Code formatting check with black
3. Static Type checked with mypy
4. unit tests for public functions/classes
5. integration tests between different interfaces
6. unit tests and integration tests are placed in the tests folder and are named as follows:
     - unit tests: test_folder_file_function/class_unit.py
     - integration tests: test_folder_file_function/class_integration.py
7. Coverage of how much of the code is tested with unit tests and integration tests
8. No print output, everything is output via log statements
9. Automatic verification via CI/CD pipeline

# Description of the data

Images in size 32x32 and in RGB from the <a href="https://www.cs.toronto.edu/~kriz/cifar.html">CIFAR-10 dataset</a> are used as data.

## Labels and Description

Here is a table of labels and descriptions:

| Label | Description |
| --- | --- |
| 0 | airplane |
| 1 | automobile |
| 2 | bird |
| 3 | cat |
| 4 | deer |
| 5 | dog |
| 6 | frog |
| 7 | horse |
| 8 | ship |
| 9 | truck |

## Data Examples
Here's an example of how the data looks:

![](readme_files/cifar10_example.png)

[image source](https://www.cs.toronto.edu/~kriz/cifar.html)

## Dataset Citation
[Learning Multiple Layers of Features from Tiny Images](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf), Alex Krizhevsky, 2009.
