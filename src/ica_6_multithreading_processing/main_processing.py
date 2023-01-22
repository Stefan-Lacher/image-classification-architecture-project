"""
this file uses multithreading to listen to the websocket server,
processing, analysing images and calculation of the end results
"""

# pylint: disable=C0413, E0401

import sys
import os
import logging
import threading
import queue


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from ica_3_image_processing.main_image_processing import ImageProcessor  # type: ignore


class MainSession:
    """
    This is the class for the main session
    The multithreading operations happen here
    """

    def __init__(self) -> None:
        # Create the needed queues
        self.message_queue: queue.Queue = queue.Queue()
        self.analysis_message_queue: queue.Queue = queue.Queue()

        # Create listener thread
        self.listener_thread = threading.Thread(target=self.message_listener)

        # Create processor thread
        self.analyzer_thread = threading.Thread(target=self.message_analyzer)

        # Create calculation thread
        self.calculator_thread = threading.Thread(target=self.message_calculation)

        # Start both threads
        self.listener_thread.start()
        self.analyzer_thread.start()
        self.calculator_thread.start()

    # Thread function for listener thread
    def message_listener(self):
        """listenes for messages"""
        ImageProcessor(image_message_queue=self.message_queue)

    # Thread function for analyzer thread
    def message_analyzer(self):
        """analyzes the messages"""

    # Thread function for calculation thread
    def message_calculation(self):
        """calculates the end results of the messages"""


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s %(filename)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
        handlers=[logging.StreamHandler(), logging.FileHandler("logging_file.log")],
    )
    logger = logging.getLogger(__name__)
    logging.warning("Configured logger")

    ##################

    MainSession()
