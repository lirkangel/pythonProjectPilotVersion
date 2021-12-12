FROM python:3.9-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && pip install pipenv && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

COPY . /app

CMD ["python3", "main.py"]
