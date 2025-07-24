import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# File paths inside Docker container
DATA_PATH = "/data/human_week7_17_Liver_Genes_TFs_lowcutoff.csv"
OUTPUT_PATH = "/data/pca_results.csv"

# Load data
df = pd.read_csv(DATA_PATH)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Optional: print to verify (can comment this out later)
print("Columns:", df.columns.tolist())

# Drop metadata columns safely
metadata_cols = ["cell", "source", "week"]
df_numeric = df.drop(columns=[col for col in metadata_cols if col in df.columns], errors='ignore')

# Drop rows with NaNs
df_numeric = df_numeric.dropna()

# Standardize
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_numeric)

# Perform PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_data)

# Build PCA DataFrame
df_pca = pd.DataFrame(pca_result, columns=["PC1", "PC2"])

# Optionally append metadata if available
for col in metadata_cols:
    if col in df.columns:
        df_pca[col] = df[col].values

# Save result
df_pca.to_csv(OUTPUT_PATH, index=False)

print("✅ PCA complete. Saved to:", OUTPUT_PATH)

