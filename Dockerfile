# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock* ./

RUN pipenv install --system --dev

COPY src .

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]