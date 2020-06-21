FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y libenchant-dev
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
