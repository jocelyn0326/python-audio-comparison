# Pull base image
FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONBREAKPOINT=ipdb.set_trace

WORKDIR /code/

# Install dependencies
COPY poetry.lock /
COPY pyproject.toml .
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . /code/

EXPOSE 8000
