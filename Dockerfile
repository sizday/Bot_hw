FROM ubuntu:latest
RUN apt-get install -y libenchant-dev
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
