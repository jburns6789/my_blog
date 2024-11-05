FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /my_blog

COPY Pipfile Pipfile.lock /my_blog/
RUN pip install pipenv && pipenv install --system

COPY . /my_blog/