FROM ubuntu:latest
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN apt-get update -y
RUN apt-get install -y libenchant1c2a
RUN pip install -r requirements.txt
