FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install enchant
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
