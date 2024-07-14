FROM python:3.10-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY pipfile.txt /app/pipfile.txt

RUN pip install --no-cache-dir -r /app/pipfile.txt

COPY . /app