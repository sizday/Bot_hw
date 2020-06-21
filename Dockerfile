FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN sudo apt-get install -y libenchant-dev
RUN pip install -r requirements.txt
