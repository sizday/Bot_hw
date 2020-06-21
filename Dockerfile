FROM ubuntu:latest
RUN apt-get install -y python3-enchant
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
