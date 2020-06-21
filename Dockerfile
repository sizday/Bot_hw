FROM ubuntu:latest
RUN sudo apt-get install -y enchant
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
