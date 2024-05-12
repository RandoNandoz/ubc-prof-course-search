# syntax=docker/dockerfile:1

FROM python:latest

COPY . /app

RUN pip install -r /app/requirements.txt

WORKDIR /app
CMD gunicorn -b 0.0.0.0:80 -w 17 app:app
