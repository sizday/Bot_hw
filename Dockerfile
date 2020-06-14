FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN python -m pip install --upgrade pip
RUN sudo apt-get install libenchant1c2a
RUN pip install -r requirements.txt
