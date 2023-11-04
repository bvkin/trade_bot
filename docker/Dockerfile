FROM python:3.11.4-slim

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir . --upgrade pip

CMD ["python", "trade_bot/main.py"]
