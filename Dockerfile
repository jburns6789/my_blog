FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /my_blog

RUN pip install --upgrade pip && \
    pip install pipenv

COPY Pipfile Pipfile.lock /my_blog/
RUN pipenv install --system --deploy

COPY . /my_blog/