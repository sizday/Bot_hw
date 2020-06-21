FROM python:latest
FROM alpine:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN apk add libenchant-dev
RUN pip install -r requirements.txt
