FROM python:3.11-slim

ENV PYTHONUNBUFFERED=True

WORKDIR /app

# Using an existing requirements file if it exists, otherwise just fastapi uvicorn
COPY . .
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir --default-timeout=1000 --retries=10 -r requirements.txt; fi

EXPOSE 8003

# assuming api.py or main.py is the entry point (metadata shows api.py)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]
