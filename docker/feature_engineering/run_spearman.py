import os
import pandas as pd
import numpy as np
import boto3

def download_from_s3(s3_path, local_path):
    print(f"📦 Downloading from S3: {s3_path} to {local_path}")
    s3 = boto3.client('s3')
    parts = s3_path.replace("s3://", "").split("/", 1)
    bucket = parts[0]
    key = parts[1]
    s3.download_file(bucket, key, local_path)
    return local_path

def main():
    # ENV inputs
    INPUT_PATH = os.environ.get("INPUT_PATH", "data/expression_matrix.csv")
    OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "data/spearman_results.csv")

    LOCAL_EXPR = "input_data.csv"

    if INPUT_PATH.startswith("s3://"):
        INPUT_PATH = download_from_s3(INPUT_PATH, LOCAL_EXPR)

    print(f"🔍 Loading expression matrix from: {INPUT_PATH}")
    df_expr = pd.read_csv(INPUT_PATH, index_col=0)
    df_expr.columns = df_expr.columns.str.strip().str.lower()

    print(f"Data shape: {df_expr.shape}")

    # Drop rows with NaNs
    df_expr = df_expr.dropna()
    print(f"Dropped rows with NaNs. New shape: {df_expr.shape}")

    # Compute Spearman correlation between genes (columns)
    print("Computing Spearman correlation...")
    spearman_corr = df_expr.corr(method='spearman')

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    spearman_corr.to_csv(OUTPUT_PATH)

    print(f"✅ Spearman correlation matrix saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

