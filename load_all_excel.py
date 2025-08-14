import pandas as pd
import os

print("Starting load_all_excel.py...")

# Check and create output directory if needed
output_dir = "../output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")

data_folder = "../data"

# Check if data folder exists
if not os.path.exists(data_folder):
    print(f"ERROR: Data folder '{data_folder}' does not exist!")
    print("Make sure your CSV files are in the '../data' folder")
    exit()

# List all CSV files in data folder
all_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

if not all_files:
    print(f"ERROR: No CSV files found in {data_folder}")
    print("Make sure you have CSV files in the data folder")
    exit()

print(f"Found {len(all_files)} CSV files: {all_files}")

df_list = []

for file in all_files:
    file_path = os.path.join(data_folder, file)
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path, encoding='latin1')  # use latin1 encoding
        df['source_file'] = file  # track origin file
        df_list.append(df)
        print(f"  ✅ Successfully loaded {len(df)} rows from {file}")
    except Exception as e:
        print(f"  ❌ Error loading {file}: {e}")

if not df_list:
    print("ERROR: No files were loaded successfully!")
    exit()

# Combine all DataFrames
print("\nCombining all data...")
combined_df = pd.concat(df_list, ignore_index=True)

print(f"✅ Combined data shape: {combined_df.shape}")
print(f"✅ Total columns: {len(combined_df.columns)}")
print(f"✅ Column names: {combined_df.columns.tolist()}")

print("\nFirst 5 rows of combined data:")
print(combined_df.head())

# Save combined data
output_file = os.path.join(output_dir, "combined_uber_data.csv")
try:
    combined_df.to_csv(output_file, index=False)
    print(f"\n✅ SUCCESS: Saved combined data to {output_file}")
    print(f"✅ File size: {os.path.getsize(output_file)} bytes")
except Exception as e:
    print(f"❌ ERROR saving file: {e}")
    exit()

print("\n🎉 load_all_excel.py completed successfully!")