FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
