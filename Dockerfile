FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install libenchant-dev
RUN pip install -r requirements.txt
