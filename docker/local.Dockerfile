FROM python:3.10.12-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN pip install --upgrade pip
ADD requirements/ requirements/
RUN pip --disable-pip-version-check install -r requirements/local.txt

COPY .. /app
