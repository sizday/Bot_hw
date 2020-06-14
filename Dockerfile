FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install --no-binary pyenchant
RUN pip install -r requirements.txt
