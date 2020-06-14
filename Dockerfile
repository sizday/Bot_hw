FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN python -m pip install --upgrade pip
RUN sudo apt update
RUN sudo apt install hunspell-ru
RUN sudo apt install hunspell-en
RUN pip install -r requirements.txt
