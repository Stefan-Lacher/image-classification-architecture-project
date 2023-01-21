"""This is the websocket server"""

# pylint: disable=W0621, W0613, E0401

import websocket_server  # type: ignore
from websocket_server import WebsocketServer


def new_client(client, server):
    """on new client"""
    print(f"New client connected {client}")


def client_left(client, server):
    """on disconnect of the client"""
    print(f"client disconnected {client}")


def message_received(client, server, message):
    """on messages"""
    print(f"Client: {client} send the message: {message}")
    server.send_message_to_all(f"Client: {client} send the message: {message}")


server = WebsocketServer(
    host="localhost", port=8765, loglevel=websocket_server.logging.INFO
)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
