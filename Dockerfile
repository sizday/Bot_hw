FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
FROM alpine:3.7
RUN apk add --no-cache libenchant
