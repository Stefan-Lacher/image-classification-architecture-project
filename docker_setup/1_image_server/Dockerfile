FROM python:3.9

COPY src/2_image_stream/image_server /src/2_image_stream/image_server
WORKDIR /src/2_image_stream/image_server

RUN pip3 install websocket-server==0.6.4

ENTRYPOINT python3 main_image_server.py
