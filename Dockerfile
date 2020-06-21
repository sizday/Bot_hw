FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y libenchant
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
