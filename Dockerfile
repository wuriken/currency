FROM python:3.7.2

RUN apt-get update && apt-get install -y --no-install-recommends \
    python-dev \
    python-setuptools

WORKDIR /srv/project

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
