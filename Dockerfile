FROM python:latest
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN apt-get install -y libenchant1c2a
RUN pip install -r requirements.txt
