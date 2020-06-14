FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN python -m pip install --upgrade pip
RUN pip install libenchant1e2a
RUN pip install -r requirements.txt
