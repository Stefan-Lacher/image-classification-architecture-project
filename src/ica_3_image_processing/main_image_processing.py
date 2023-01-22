"""this file listens to the websocket server"""

# pylint: disable=R0903, W0613, C0103, W0621

import sys
import os
import logging
import queue
import websocket  # type: ignore


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class ImageProcessor:
    """
    listens to the Websocket Server for messages,
    processes the messages and writes them into a queue
    """

    def __init__(self, image_message_queue: queue.Queue) -> None:
        self.image_message_queue = image_message_queue
        websocket.enableTrace(True)
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
        logging.info("Connection closed.")

    def _on_open(self, ws):
        """on connection open send image messages"""
        logging.info("Connection opened.")
