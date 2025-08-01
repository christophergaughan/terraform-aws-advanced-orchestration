# Base image: slim to keep it light
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && \
    apt-get install -y build-essential gcc libglib2.0-0 libsm6 libxrender1 libxext6 curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the feature engineering scripts into the container
COPY feature_engineering/ ./feature_engineering/

# Set the working directory to the script folder
WORKDIR /app/feature_engineering

# Default command (can be overridden at runtime)
CMD ["python", "run_pca.py"]

