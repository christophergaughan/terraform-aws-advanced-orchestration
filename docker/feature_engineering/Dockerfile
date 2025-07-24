# docker/feature_engineering/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Copy your script into the container
COPY run_pca.py .

# Install required libraries
RUN pip install pandas scikit-learn pyarrow numpy

# Run the feature engineering script by default
CMD ["python", "run_pca.py"]

