import pandas as pd
import os

print("Starting data_cleaning.py...")

# Check if input file exists
input_file = "../output/combined_uber_data.csv"
if not os.path.exists(input_file):
    print(f"ERROR: {input_file} not found!")
    print("Please run load_all_excel.py first to create the combined data file.")
    exit()

# Load combined data
print(f"Loading data from {input_file}...")
try:
    df = pd.read_csv(input_file, low_memory=False)
    print(f"✅ Loaded data with shape: {df.shape}")
    print(f"✅ Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"ERROR loading data: {e}")
    exit()

print("\nOriginal data sample:")
print(df.head())

# Get initial data info
initial_rows = len(df)
print(f"\nInitial data info:")
print(f"- Rows: {initial_rows}")
print(f"- Columns: {len(df.columns)}")

# FIX: Handle duplicate column names by making them unique
print("\nFixing duplicate column names...")
df.columns = pd.io.common.dedup_names(df.columns, is_potential_multiindex=False)
print(f"✅ Fixed duplicate column names")

# Now find the best DATE and TIME columns
print("\nLooking for date and time columns...")
date_columns = [col for col in df.columns if 'date' in col.lower() and df[col].notna().sum() > 1000]
time_columns = [col for col in df.columns if 'time' in col.lower() and df[col].notna().sum() > 1000]

print(f"Found date columns with data: {date_columns}")
print(f"Found time columns with data: {time_columns}")

# Pick the columns with the most data
if date_columns and time_columns:
    # Find the date and time columns with most non-null values
    best_date_col = max(date_columns, key=lambda x: df[x].notna().sum())
    best_time_col = max(time_columns, key=lambda x: df[x].notna().sum())
    
    print(f"Using date column: {best_date_col} ({df[best_date_col].notna().sum()} values)")
    print(f"Using time column: {best_time_col} ({df[best_time_col].notna().sum()} values)")
    
    print("\nCleaning data...")
    
    # Create pickup_datetime using the best columns
    print("Creating pickup_datetime column...")
    df['pickup_datetime'] = pd.to_datetime(
        df[best_date_col].astype(str) + ' ' + df[best_time_col].astype(str), 
        errors='coerce'
    )
    
    # Check how many datetime conversions worked
    valid_datetimes = df['pickup_datetime'].notna().sum()
    invalid_datetimes = df['pickup_datetime'].isna().sum()
    print(f"✅ Created pickup_datetime: {valid_datetimes:,} valid, {invalid_datetimes:,} invalid")
    
    # Remove rows with invalid datetime
    df = df.dropna(subset=['pickup_datetime'])
    print(f"✅ Removed {initial_rows - len(df):,} rows with invalid datetime")
    
    # Remove duplicates
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dedup - len(df)
    print(f"✅ Removed {duplicates_removed:,} duplicate rows")
    
else:
    print("⚠️  Warning: Could not find suitable date/time columns with sufficient data")
    print("Available columns:", df.columns.tolist()[:10], "...")  # Show first 10
    print("Performing basic cleaning without datetime processing...")
    
    # Just remove duplicates if we can't process datetime
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dedup - len(df)
    print(f"✅ Removed {duplicates_removed:,} duplicate rows")

print(f"\nCleaned data sample:")
print(df.head())

print(f"\nFinal data info:")
print(f"- Rows: {len(df):,} (reduced by {initial_rows - len(df):,})")
print(f"- Columns: {len(df.columns)}")

# Save cleaned data
output_file = "../output/cleaned_uber_data.csv"
try:
    print(f"\nSaving cleaned data (this may take a few minutes for large data)...")
    df.to_csv(output_file, index=False)
    print(f"✅ SUCCESS: Saved cleaned data to {output_file}")
    file_size_mb = os.path.getsize(output_file) / 1024 / 1024
    print(f"✅ File size: {file_size_mb:.1f} MB")
except Exception as e:
    print(f"ERROR saving cleaned data: {e}")
    exit()

print("\n🎉 data_cleaning.py completed successfully!")