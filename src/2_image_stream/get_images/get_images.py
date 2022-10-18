"""gets images from dataset for the image stream"""

# pylint: disable=E0401, R0903, W1203


import logging
import os
import pickle
import shutil
import sys
import tarfile

import matplotlib.pyplot as plt  # type: ignore
from torchvision.datasets.utils import download_url  # type: ignore

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

BASE_DIR = "src/2_image_stream/get_images"

class CreateImages:
    """everything for creating an image dataset"""

    def __init__(self, classes, folder_name, total_images_batch) -> None:
        self.classes = classes
        self.folder_name = f"{BASE_DIR}/{folder_name}"
        self.total_images_batch = total_images_batch

    def _download_dataset(
        self, dataset_url="https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
    ) -> str:
        """downloads the dataset"""
        logging.info("started download dataset")
        saving_path = f"{self.folder_name}"
        os.mkdir(saving_path)
        logging.info(f"download dataset created folder: {saving_path}")
        download_url(dataset_url, saving_path)
        logging.info("downloaded dataset")
        dataset_name = dataset_url.split("/")[-1]
        dataset_path = f"{saving_path}/{dataset_name}"
        logging.info("created dataset path")
        return dataset_path

    def _delete_downloaded_dataset(
        self, dataset_name, batch_folder_name="cifar-10-batches-py") -> None:
        """deletes downloaded dataset after saving images"""
        logging.info("started delete dataset")
        os.remove(dataset_name)
        shutil.rmtree(f"{self.folder_name}/{batch_folder_name}")
        logging.info("removed downloaded dataset, without the saved images")

    def _extract_batches(self, dataset_name):
        """extracts batches from gz file"""
        logging.info("started extracting batches")
        with tarfile.open(dataset_name, "r:gz") as tar:
            tar.extractall(path=f"{self.folder_name}")
        logging.info("finished extracting batches")

    def _unpickle_batches(self, batch_folder_name="cifar-10-batches-py"):
        """Load byte data from file"""
        logging.info("started unpack pickles")
        first_path = f"{self.folder_name}/{batch_folder_name}"
        data_list = []
        for batch in os.listdir(first_path):
            if "batch" in batch and "meta" not in batch:
                print(batch)
                path_creation = f"{first_path}/{batch}"
                with open(path_creation, "rb") as batch_file:
                    data = pickle.load(batch_file, encoding="latin1")
                    data_list.append(data)
        logging.info("finished unpack pickles and returned data_list")
        return data_list

    def _create_folders(self, data_list):
        """creates the folders for saving the data"""
        logging.info("started creating folders")
        path = f"{self.folder_name}"
        for data in data_list:
            batch_label = data["batch_label"]
            batch_label = batch_label.replace(" ", "_")
            new_path = f"{path}/{batch_label}"
            os.mkdir(new_path)
            for j, k in enumerate(self.classes):
                end_path = f"{new_path}/{j}_{k}"
                os.mkdir(end_path)
        logging.info("created all folders")

    def _saving_files(self, data_list):
        """saving files"""
        logging.info("started saving files")
        for data in data_list:
            batch_label = data["batch_label"]
            batch_label = batch_label.replace(" ", "_")
            batch_images = data["data"]
            batch_names = data["filenames"]
            batch_labels = data["labels"]
            for j in range(self.total_images_batch):
                image_pick = batch_images[j]
                name_pick = batch_names[j]
                label_pick = batch_labels[j]
                transformed_img = image_pick.reshape(3, 32, 32).transpose([1, 2, 0])
                saving_path = (
                    f"{self.folder_name}/{batch_label}/"
                    f"{label_pick}_{self.classes[label_pick]}/"
                    f"{label_pick}_{name_pick}"
                )
                plt.imsave(saving_path, transformed_img)
        logging.info("saved all defined files")

    def create_images_complete(self) -> None:
        """the complete saving part"""
        logging.info("started the complete function")
        dataset_name = self._download_dataset()
        self._extract_batches(dataset_name=dataset_name)
        data_list = self._unpickle_batches()
        self._create_folders(data_list=data_list)
        self._saving_files(data_list=data_list)
        self._delete_downloaded_dataset(dataset_name=dataset_name)
        logging.info("everything is completed")


def get_images():
    """main function of get images"""
    class_names = (
        "plane",
        "car",
        "bird",
        "cat",
        "deer",
        "dog",
        "frog",
        "horse",
        "ship",
        "truck",
    )
    saving_folder = "dataset_batches_test"
    total_images_per_batch = 100
    logging.info(f"defined classes: {class_names}")
    logging.info(f"defined saving folder: {saving_folder}")
    logging.info(f"defined images per batch: {total_images_per_batch}")

    save_defined_images = CreateImages(
        classes=class_names,
        folder_name=saving_folder,
        total_images_batch=total_images_per_batch,
    )
    save_defined_images.create_images_complete()


# run main code
if __name__ == "__main__":
    #################### logging ####################

    LOG_FILE_NAME = f"{BASE_DIR}/logging_file_get_images.log"

    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE_NAME),
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("Test log statement")
    logger.info(f"current log file: {LOG_FILE_NAME}")

    #################### start main ####################
    get_images()
