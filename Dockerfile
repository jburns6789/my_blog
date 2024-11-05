FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /my_blog

COPY Pipfile Pipfile.lock /my_blog/
RUN pip install pipenv && pipenv install --system

COPY . /my_blog/