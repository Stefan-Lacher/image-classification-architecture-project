FROM python:3.9

COPY src/ica_2_image_stream/image_server /src/ica_2_image_stream/image_server
WORKDIR /src/ica_2_image_stream/image_server

RUN pip3 install -r requirements_image_server.txt

ENTRYPOINT python3 main_image_server.py
