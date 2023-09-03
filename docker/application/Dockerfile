FROM python:3.10-alpine3.16

WORKDIR /file_processing

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apk add postgresql-client build-base postgresql-dev

RUN adduser --disabled-password web-user
USER web-user