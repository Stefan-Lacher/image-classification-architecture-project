"""This pipeline loads the images, prepares them and converts them for sending"""

# pylint: disable=C0413, E0401, R0903, E1101

import sys
import os
import logging
import base64
import cv2  # type: ignore


# import msgpack  # type: ignore

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from get_images.get_images import get_images  # type: ignore


class ImagePipeline:
    """this class is the image pipeline"""

    def __init__(self, file_list: list, image_list: list) -> None:
        """init of ImagePipeline Class"""

        logging.info("Checks if images are there")
        path_list: list = os.listdir("get_images")
        if "dataset_batches_test" in path_list:
            logging.info("get_images is true")
        else:
            logging.info("get_images is false")
            get_images()

        # Load all images in memory
        self.batch_path: str = os.path.join("get_images", "dataset_batches_test")
        logging.info("iterate threw directory for image paths")
        self._iterate_directory(path=self.batch_path, path_list=file_list)
        logging.info("iterate threw file list to prepare the images for sending")
        self._image_preperation(file_list=file_list, image_list=image_list)

    def _image_preperation(self, file_list: list, image_list: list) -> None:
        """prepares the images and converts them for sending"""
        for image in file_list:
            np_array = cv2.imread(image, cv2.IMREAD_COLOR)
            encoded_image = base64.b64encode(np_array)
            string_data = encoded_image.decode("utf-8")
            image_list.append(string_data)

    def _iterate_directory(self, path: str, path_list: list) -> None:
        """iterate threw directory with scandir"""
        for item in os.scandir(path):
            if item.is_file():
                path_list.append(item.path)
            elif item.is_dir():
                self._iterate_directory(item.path, path_list)
