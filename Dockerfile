FROM alpine:3.7
RUN apk add -y libenchant-dev
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
