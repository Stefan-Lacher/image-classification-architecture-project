FROM python:3.9

COPY src/ica_2_image_stream /src/ica_2_image_stream
WORKDIR /src/ica_2_image_stream

RUN pip3 install -r requirements_send_images.txt

ENTRYPOINT python3 send_images/main_image_sender.py