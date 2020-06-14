FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN python -m pip install --upgrade pip
RUN sudo apt install hunspell-ru
RUN pip install -r requirements.txt
