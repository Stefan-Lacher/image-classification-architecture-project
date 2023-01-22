"""
this file uses multithreading to listen to the websocket server,
processing, analysing images and calculation of the end results
"""

# pylint: disable=C0413

import sys
import os

# import logging


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
for i in sys.path:
    print(i)

# from ica_3_image_processing.main_image_processing import ImageProcessor

# if __name__ == "__main__":
#     logging.basicConfig(
#         format="%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s %(filename)s - %(message)s",
#         datefmt="%H:%M:%S",
#         level=logging.INFO,
#         handlers=[logging.StreamHandler(), logging.FileHandler("logging_file.log")],
#     )
#     logger = logging.getLogger(__name__)
#     logging.warning("Configured logger")
