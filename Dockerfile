# FROM python:3.9-alpine3.13
FROM python:3.9-slim-bullseye
LABEL maintainer="to-be-defined"

RUN apt-get update &&  apt-get upgrade -y

ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --no-create-home django-user

COPY ./requirements.txt /tmp/requirements.txt
# COPY ./app /app
# WORKDIR /app
EXPOSE 8000

# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r /tmp/requirements.txt && \
#     rm -rf /tmp && \
#     adduser \
#         --disabled-password \
#         django-user

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt

RUN rm -rf /tmp

ENV PATH="/py/bin:$PATH"

COPY ./app /app
WORKDIR /app

USER django-user