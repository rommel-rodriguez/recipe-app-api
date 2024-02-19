# FROM python:3.9-alpine3.13
FROM python:3.9-slim-bullseye
LABEL maintainer="to-be-defined"

ARG DEV=false
RUN apt-get -qq update &&  apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3-dev libpq-dev

# Pillow dependencies: https://pillow.readthedocs.io/en/stable/installation.html
# Specific for Debian 11 bullseye:
#   https://github.com/python-pillow/docker-images/blob/main/debian-11-bullseye-amd64/Dockerfile
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    cmake \
    curl \
    ghostscript \
    git \
    libffi-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    libjpeg-turbo-progs \
    libjpeg62-turbo-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    libwebp-dev \
    libssl-dev \
    meson \
    netpbm \
    python3-dev \
    python3-numpy \
    python3-setuptools \
    python3-tk \
    sudo \
    tcl8.6-dev \
    tk8.6-dev \
    virtualenv \
    wget \
    xvfb \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


# uWSGI requirement
# RUN DEBIAN_FRONTEND=noninteractive apt-get -y install linux-headers-$(uname -r)

ENV PYTHONUNBUFFERED 1

RUN adduser --disabled-password --no-create-home django-user

# Create directoy for static and media files
RUN mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts

# Enable execute rights on script directory
RUN chmod -R +x /scripts

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

CMD ["run.sh"]