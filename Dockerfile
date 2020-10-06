FROM python:3.8.1-slim-buster
COPY requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

WORKDIR /code
COPY logging* ./
COPY src/manage.py ./manage.py

WORKDIR /code/src
COPY src .
