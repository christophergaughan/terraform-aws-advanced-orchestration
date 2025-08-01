import os
import pandas as pd
import numpy as np
import boto3

def download_from_s3(s3_path, local_path):
    print(f"📦 Downloading from S3: {s3_path} to {local_path}")
    s3 = boto3.client('s3')
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    s3.download_file(bucket, key, local_path)
    return local_path

def upload_to_s3(local_path, s3_path):
    print(f"☁️ Uploading {local_path} to {s3_path}")
    s3 = boto3.client('s3')
    bucket, key = s3_path.replace("s3://", "").split("/", 1)
    s3.upload_file(local_path, bucket, key)
    print("✅ Upload complete.")

def is_mitochondrial(gene_name):
    return gene_name.upper().startswith("MT-")

def main():
    INPUT_PATH = os.environ.get("INPUT_PATH", "expression_matrix.csv")
    OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "expression_matrix_qc_filtered.csv")
    S3_OUTPUT_PATH = os.environ.get("S3_OUTPUT_PATH")

    MIN_GENES = int(os.environ.get("MIN_GENES", 200))
    MAX_GENES = int(os.environ.get("MAX_GENES", 5000))
    MAX_MITO_PCT = float(os.environ.get("MAX_MITO_PCT", 20.0))

    LOCAL_EXPR = "raw_expr.csv"
    if INPUT_PATH.startswith("s3://"):
        INPUT_PATH = download_from_s3(INPUT_PATH, LOCAL_EXPR)

    print(f"🔍 Loading expression matrix from: {INPUT_PATH}")
    df = pd.read_csv(INPUT_PATH, index_col=0)

    print("🧬 Calculating QC metrics...")
    total_counts = df.sum(axis=1)
    num_genes = (df > 0).sum(axis=1)

    mito_genes = [col for col in df.columns if is_mitochondrial(col)]
    mito_counts = df[mito_genes].sum(axis=1)
    mito_pct = mito_counts / total_counts * 100

    qc_df = pd.DataFrame({
        "total_counts": total_counts,
        "num_genes": num_genes,
        "mito_pct": mito_pct
    })

    # Apply filters
    keep = (
        (qc_df["num_genes"] >= MIN_GENES) &
        (qc_df["num_genes"] <= MAX_GENES) &
        (qc_df["mito_pct"] <= MAX_MITO_PCT)
    )
    df_filtered = df.loc[keep]

    print(f"✅ Filtered from {df.shape[0]} → {df_filtered.shape[0]} cells")

    df_filtered.to_csv(OUTPUT_PATH)
    print(f"📁 Saved filtered matrix to {OUTPUT_PATH}")

    if S3_OUTPUT_PATH:
        upload_to_s3(OUTPUT_PATH, S3_OUTPUT_PATH)

if __name__ == "__main__":
    main()

