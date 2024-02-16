# FROM python:3.9-alpine3.13
FROM python:3.9-slim-bullseye
LABEL maintainer="to-be-defined"

ARG DEV=false
RUN apt-get update &&  apt-get upgrade -y

RUN apt-get install -y build-essential python3-dev libpq-dev

ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --no-create-home django-user

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

RUN apt-get -y clean && apt-get -y autoremove 

RUN /py/bin/pip install -r /tmp/requirements.txt


RUN if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi

RUN rm -rf /tmp

ENV PATH="/py/bin:$PATH"

COPY ./app /app
WORKDIR /app

USER django-user
