FROM python:3.9

COPY src/2_image_stream/send_images /src/2_image_stream/send_images
WORKDIR /src/2_image_stream/send_images

RUN pip3 install websocket-client==1.4.2

ENTRYPOINT python3 main_image_sender.py