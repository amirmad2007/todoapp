FROM docker.arvancloud.ir/python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt .
RUN pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip && \
    pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY . .
