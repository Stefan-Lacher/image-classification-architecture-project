# Image Stream folder

This is the description for the folder Image Stream.

The technical subfolder contain several scripts that work together to create a WebSocket server and download, prepare, and send image datasets to a WebSocket server. 


## Technical subfolder description

---
### get_images

This script get_images.py creates an image dataset by downloading a dataset from a URL, extracting the images, and saving them to a new folder.

The CreateImages class contains methods for downloading, extracting, and saving the dataset images. The get_images() function defines the classes of images to download and the folder to save the images to.

The CreateImages class has several methods:

_download_dataset() downloads the dataset from a given URL and saves it to the specified folder.
_extract_batches() extracts batches from the dataset's gz file.
_unpickle_batches() loads the data from the batches.
_create_folders() creates the folders for the downloaded data.
_saving_files() saves the images to the specified folder.
_delete_downloaded_dataset() deletes the downloaded dataset after the images are saved.
The get_images() function defines the classes of images to download and the folder to save the images to. It then creates an instance of the CreateImages class with these parameters and runs the create_images_complete() method, which downloads the dataset, extracts the images, creates folders for the images, saves the images, and deletes the downloaded dataset.

The script uses the logging library to log information about the process at various points. Additionally, it uses the matplotlib library to save the images.

---
### image_server

This script main_image_server.py is a simple WebSocket server that listens for incoming connections and handles messages from clients. The server is implemented using the websocket_server package.


new_client(client, server)
This function is called when a new client connects to the server. The client argument is a dictionary containing information about the client, such as its IP address and port number. The server argument is a reference to the WebsocketServer instance.

client_left(client, server)
This function is called when a client disconnects from the server. The client argument is the same dictionary as in new_client. The server argument is a reference to the WebsocketServer instance.

message_received(client, server, message)
This function is called when a message is received from a client. The client argument is the same dictionary as in new_client. The server argument is a reference to the WebsocketServer instance. The message argument is a string containing the message sent by the client.

---
### prepare_images

In the prepare_images folder and the image_pipeline.py file the ImagePipeline class defines a pipeline for loading and preparing images for sending. The class takes two arguments, file_list and image_list, which are both lists.

The constructor of the ImagePipeline class performs the following actions:

Checks if the images are already available in the "get_images" directory.
If the images are not available, it calls the get_images() function to download the images.
Sets the batch_path variable to the path of the "dataset_batches_test" directory within the "get_images" directory.
Iterates through the directory specified by the batch_path variable and appends each image's path to the file_list.
Prepares the images for sending by calling the _image_preparation() method, which converts the images to a format that can be sent.
The ImagePipeline class has two private methods:

The _image_preparation() method, which prepares the images for sending by converting them to a format that can be sent.
The _iterate_directory() method, which iterates through a directory and appends each image's path to the file_list.
The _image_preparation() method converts each image in the file_list to a NumPy array using cv2.imread(), encodes it to base64 using base64.b64encode(), and decodes it to a UTF-8 string using encoded_image.decode("utf-8"). The resulting string is then appended to the image_list.

The _iterate_directory() method iterates through a directory using os.scandir() and appends the path of each file in the directory to the path_list. If a subdirectory is encountered, the method calls itself recursively to continue the iteration.

The ImagePipeline class uses the logging library to log information about the process at various points. Additionally, it uses the cv2 library to load and prepare the images and the base64 library to encode the images for sending.

---
### send_images

In the folder send_images and the file main_image_sender.py the class ImageSender sends image messages to a WebSocket server. When an instance of this class is created, it initializes a file_list and image_list and starts the ImagePipeline from the folder prepare_images to prepare the images. Then, it shuffles the image list and establishes a WebSocket connection to a server running on localhost:8765.

The _on_message, _on_error, _on_close, and _on_open methods are callbacks that are triggered by events in the WebSocket connection.
_on_open is triggered when the WebSocket connection is opened. In this method, the image messages are sent to the server.
_on_close is triggered when the WebSocket connection is closed. In this method, the method waits for a brief moment and then logs the closure of the connection.
_on_error is triggered when an error occurs in the WebSocket connection. In this method, the error message is logged.
_on_message is triggered when a message is received from the WebSocket server. In this method, the message is logged.

The script uses the logging module to log messages at the INFO level. It also saves the logs to a file named "logging_file.log".
