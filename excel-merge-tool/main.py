import os
import glob
import pandas as pd
from utils.excel_utils import clean_and_standardize, FINAL_COLUMNS

INPUT_FOLDER = "input_files"
OUTPUT_FOLDER = "output"
OUTPUT_EXCEL = os.path.join(OUTPUT_FOLDER, "merged.xlsx")
OUTPUT_CSV = os.path.join(OUTPUT_FOLDER, "merged.csv")

# Supported file extensions
SUPPORTED_EXTENSIONS = ["*.xlsx", "*.xls", "*.xlsm", "*.xlsb", "*.csv"]

def find_all_files():
    """Find all files in the input folder matching the supported extensions."""
    all_files = []
    for ext in SUPPORTED_EXTENSIONS:
        all_files += glob.glob(os.path.join(INPUT_FOLDER, "**", ext), recursive=True)
    return all_files

def read_file(file):
    """Read Excel or CSV file into a DataFrame."""
    try:
        if file.lower().endswith(".csv"):
            # Try UTF-8 first, fallback to Latin-1
            try:
                return pd.read_csv(file, encoding="utf-8", low_memory=False)
            except UnicodeDecodeError:
                return pd.read_csv(file, encoding="latin-1", low_memory=False)
        else:
            return pd.read_excel(file, engine=None)
    except Exception as e:
        print(f"⚠️ Could not read file {file}: {e}")
        return None

def merge_files():
    """Merge all Excel and CSV files into one clean DataFrame."""
    all_files = find_all_files()

    if not all_files:
        print("❌ No supported files found in the 'input_files' directory.")
        return

    print(f"📂 Found {len(all_files)} files (all supported types), starting merge process...")
    dataframes = []

    for file in all_files:
        df = read_file(file)
        if df is not None and not df.empty:
            # Clean and standardize columns
            df = clean_and_standardize(df)
            # Add source filename column
            df["source_file"] = os.path.basename(file)
            dataframes.append(df)
            print(f"✅ Loaded: {os.path.basename(file)} ({len(df)} rows)")
        else:
            print(f"⚠️ Skipping {os.path.basename(file)} (empty or unreadable)")

    if not dataframes:
        print("❌ Failed to load any data.")
        return

    # Concatenate all DataFrames
    merged_df = pd.concat(dataframes, ignore_index=True)
    # Remove duplicate rows
    merged_df.drop_duplicates(inplace=True)
    # Replace NaN with empty string
    merged_df.fillna("", inplace=True)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    # Ensure columns in correct order + source_file last
    final_cols = FINAL_COLUMNS + ["source_file"]
    merged_df = merged_df[final_cols]

    # Save merged DataFrame to Excel and CSV
    merged_df.to_excel(OUTPUT_EXCEL, index=False)
    merged_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("\n✅ Merge completed successfully!")
    print(f"📄 Total rows in merged file: {len(merged_df)}")
    print(f"📂 Total files merged: {len(all_files)}")
    print(f"📦 Output saved as: {OUTPUT_EXCEL}")
    print(f"📦 Also saved as CSV: {OUTPUT_CSV}")

if __name__ == "__main__":
    merge_files()
