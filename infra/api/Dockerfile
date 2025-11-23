FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/api/ ./src/api/
COPY alembic/ ./alembic/
COPY alembic.ini .

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["gunicorn", "src.api.app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
