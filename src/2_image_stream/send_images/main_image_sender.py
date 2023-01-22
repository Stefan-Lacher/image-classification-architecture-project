"""this file sends image messages to the websocket server"""

# pylint: disable=C0103, W0621, W0613, W0703, W0603, R0903, C0413, E0401, W1203

import sys
import os
import time
import logging
import websocket  # type: ignore
import numpy as np


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from prepare_images.image_pipeline import ImagePipeline  # type: ignore


class ImageSender:
    """class for sending the images"""

    def __init__(self) -> None:
        self.file_list: list = []
        logging.info("created file list")
        self.image_list: list = []
        logging.info("created image list")
        logging.info("start image pipeline")
        ImagePipeline(file_list=self.file_list, image_list=self.image_list)
        logging.info("finished image pipeline")
        logging.info(f"length of the image_list: {len(self.image_list)}")
        np.random.shuffle(self.image_list)
        logging.info("shuffled the image")
        logging.info("started Websocket app on localhost and port 8765")
        ws = websocket.WebSocketApp(
            "ws://localhost:8765/",
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        ws.on_open = self._on_open
        ws.run_forever()

    def _on_message(self, ws, message):
        """on receiving a message"""
        logging.info(message)

    def _on_error(self, ws, error):
        """on error with the connection to the websocket"""
        logging.info(error)

    def _on_close(self, ws, *args):
        """on closing the connection to the websocket"""
        try:
            time.sleep(0.2)
            # ws.wait()  # wait for the connection to close
            logging.info("### closed ###")
        except AttributeError as e:
            logging.info(f"closed: {e}")

        except Exception as e:
            logging.info(e)

    def _on_open(self, ws):
        """on connection open send image messages"""
        for image_message in self.image_list:
            print(image_message)
            ws.send(image_message)
            time.sleep(0.3)
        ws.close()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s %(filename)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
        handlers=[logging.StreamHandler(), logging.FileHandler("logging_file.log")],
    )
    logger = logging.getLogger(__name__)
    logging.warning("Configured logger")

    ImageSender()
