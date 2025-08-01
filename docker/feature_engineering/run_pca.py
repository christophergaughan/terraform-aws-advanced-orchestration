import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import boto3

def download_from_s3(s3_path, local_path):
    print(f"📦 Downloading from S3: {s3_path} to {local_path}")
    s3 = boto3.client('s3')
    parts = s3_path.replace("s3://", "").split("/", 1)
    bucket = parts[0]
    key = parts[1]
    s3.download_file(bucket, key, local_path)
    return local_path

def upload_to_s3(local_path, s3_path):
    print(f"☁️ Uploading {local_path} to {s3_path}")
    s3 = boto3.client('s3')
    parts = s3_path.replace("s3://", "").split("/", 1)
    bucket = parts[0]
    key = parts[1]
    s3.upload_file(local_path, bucket, key)
    print("✅ Upload complete.")

def main():
    # ENV-based configuration
    INPUT_PATH = os.environ.get("INPUT_PATH", "expression_matrix.csv")
    METADATA_PATH = os.environ.get("METADATA_PATH", "cell_metadata.csv")
    OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "pca_results.csv")
    S3_OUTPUT_PATH = os.environ.get("S3_OUTPUT_PATH")  # optional
    N_COMPONENTS = int(os.environ.get("N_COMPONENTS", 2))

    # Local cache filenames if pulling from S3
    LOCAL_EXPR = "input_data.csv"
    LOCAL_META = "meta_data.csv"

    # Download input from S3 if needed
    if INPUT_PATH.startswith("s3://"):
        INPUT_PATH = download_from_s3(INPUT_PATH, LOCAL_EXPR)
    if METADATA_PATH.startswith("s3://"):
        METADATA_PATH = download_from_s3(METADATA_PATH, LOCAL_META)

    print(f"🔍 Loading expression data from: {INPUT_PATH}")
    df_expr = pd.read_csv(INPUT_PATH, index_col=0)

    print(f"🔍 Loading metadata from: {METADATA_PATH}")
    df_meta = pd.read_csv(METADATA_PATH)

    # Normalize column names
    df_expr.columns = df_expr.columns.str.strip().str.lower()
    df_meta.columns = df_meta.columns.str.strip().str.lower()

    # Drop rows with missing values
    df_expr = df_expr.dropna()
    print(f"🧹 Cleaned expression data shape: {df_expr.shape}")

    # Standardize features
    print(f"⚙️ Standardizing with shape: {df_expr.shape}")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_expr)

    # Run PCA
    print(f"🧠 Running PCA (n_components={N_COMPONENTS})")
    pca = PCA(n_components=N_COMPONENTS)
    pca_result = pca.fit_transform(scaled_data)
    df_pca = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(N_COMPONENTS)])

    # Append metadata if dimensions match
    if len(df_meta) == len(df_pca):
        print("🔗 Appending metadata to PCA result")
        df_pca = pd.concat([df_pca, df_meta.reset_index(drop=True)], axis=1)
    else:
        print("⚠️ Metadata not appended: row count mismatch")

    # Save to local output
    df_pca.to_csv(OUTPUT_PATH, index=False)
    print(f"📁 PCA results saved locally to: {OUTPUT_PATH}")
    print("📈 Explained variance ratio:", pca.explained_variance_ratio_)

    # Upload to S3 if desired
    if S3_OUTPUT_PATH:
        upload_to_s3(OUTPUT_PATH, S3_OUTPUT_PATH)

if __name__ == "__main__":
    main()

