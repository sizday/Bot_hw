FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install enchant
RUN pip install -r requirements.txt
