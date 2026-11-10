FROM python:3.12-slim

WORKDIR /app

COPY app.py detector.py login_logs.csv /app/

RUN python -m pip install --no-cache-dir --upgrade pip

RUN useradd --create-home appuser

RUN mkdir -p /app/reports && chown appuser:appuser /app/reports


USER appuser


CMD ["python", "app.py"]