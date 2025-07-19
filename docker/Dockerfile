# Base image: slim to keep it light
FROM python:3.10-slim

# Set timezone/env if needed
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install OS-level deps if needed (optional for scientific Python)
RUN apt-get update && \
    apt-get install -y build-essential gcc libglib2.0-0 libsm6 libxrender1 libxext6 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Default command
CMD ["python", "lambda_function.py"]

