# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Include all model, inference, and preprocessing code to support end-to-end reproducible workflows
COPY . .

# Command to run when container starts
CMD ["python", "lambda_function.py"]

