FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1

COPY poetry.lock pyproject.toml /usr/src/app/

RUN pip install "poetry==$POETRY_VERSION"

RUN apk update && apk add --no-cache libffi-dev gcc\
    musl-dev python3-dev postgresql-dev\
    && poetry config virtualenvs.create false\
    && poetry install --no-interaction --no-ansi \
    && poetry update

COPY . /usr/src/app