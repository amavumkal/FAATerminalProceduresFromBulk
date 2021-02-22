FROM public.ecr.aws/lambda/python:3.8
WORKDIR /app
COPY src .
ARG DEBIAN_FRONTEND=noninteractive
RUN yum update && yum -y ImageMagick-devel && pip install -r requirements.txt
