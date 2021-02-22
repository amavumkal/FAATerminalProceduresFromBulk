FROM public.ecr.aws/lambda/python:3.8
WORKDIR /app
COPY . .
ARG DEBIAN_FRONTEND=noninteractive
RUN yum update && yum -y imagemagick && pip install -r requirements.txt
