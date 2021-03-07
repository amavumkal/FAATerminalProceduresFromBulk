
FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
ARG FUNCTION_DIR="/function"
RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY src/ ${FUNCTION_DIR}/
COPY requirements.txt ${FUNCTION_DIR}/
RUN pip3 install -r ${FUNCTION_DIR}/requirements.txt
COPY policy.xml /etc/ImageMagick-6/

WORKDIR ${FUNCTION_DIR}
RUN echo $MAGICK_CONFIGURE_PATH

CMD ["python3 app.py"]

