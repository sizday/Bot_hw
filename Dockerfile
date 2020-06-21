FROM alpine:3.7
RUN apk --no-cache add enchant
FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
