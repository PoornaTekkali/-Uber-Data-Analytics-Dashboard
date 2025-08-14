import pandas as pd
import os

print("Starting data_transformation.py...")

# Check if input file exists (can use either combined or cleaned data)
cleaned_file = "../output/cleaned_uber_data.csv"
combined_file = "../output/combined_uber_data.csv"

# Try to use cleaned data first, fall back to combined data
if os.path.exists(cleaned_file):
    input_file = cleaned_file
    print(f"Using cleaned data: {input_file}")
elif os.path.exists(combined_file):
    input_file = combined_file
    print(f"Using combined data: {input_file}")
    print("⚠️  Recommendation: Run data_cleaning.py first for better results")
else:
    print("ERROR: No input data found!")
    print("Please run load_all_excel.py (and optionally data_cleaning.py) first.")
    exit()

# Load the data CSV
print(f"Loading data from {input_file}...")
try:
    df = pd.read_csv(input_file, low_memory=False)
    print(f"✅ Loaded data with shape: {df.shape}")
except Exception as e:
    print(f"ERROR loading data: {e}")
    exit()

# Check columns available
print(f"✅ Columns in the dataset: {df.columns.tolist()}")

# Transform data based on what columns we have
if 'pickup_datetime' in df.columns:
    print("✅ pickup_datetime column already exists")
    
    # Ensure it's in datetime format
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
    valid_datetime = df['pickup_datetime'].notna().sum()
    print(f"✅ Validated pickup_datetime: {valid_datetime} valid entries")
    
elif 'DATE' in df.columns and 'TIME' in df.columns:
    print("Creating pickup_datetime from DATE and TIME columns...")
    
    # Create pickup_datetime column by combining DATE and TIME
    df['pickup_datetime'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'], errors='coerce')
    
    # Check conversion success
    valid_datetime = df['pickup_datetime'].notna().sum()
    invalid_datetime = df['pickup_datetime'].isna().sum()
    print(f"✅ Created pickup_datetime: {valid_datetime} valid, {invalid_datetime} invalid")
    
else:
    print("⚠️  Warning: No date/time columns found for pickup_datetime")
    print("Available columns:", df.columns.tolist())
    # Create a placeholder pickup_datetime
    df['pickup_datetime'] = pd.NaT

# Add additional transformed columns
print("\nAdding additional columns...")

# Since there is no dropoff time in the data, create placeholder columns
df['dropoff_datetime'] = pd.NaT
print("✅ Added dropoff_datetime (placeholder)")

df['trip_duration_mins'] = None
print("✅ Added trip_duration_mins (placeholder)")

# Add some useful derived columns if we have pickup_datetime
if 'pickup_datetime' in df.columns and df['pickup_datetime'].notna().sum() > 0:
    print("Creating additional time-based columns...")
    
    # Extract date components
    df['pickup_date'] = df['pickup_datetime'].dt.date
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day_of_week'] = df['pickup_datetime'].dt.day_name()
    df['pickup_month'] = df['pickup_datetime'].dt.month
    
    print("✅ Added pickup_date, pickup_hour, pickup_day_of_week, pickup_month")

# Show sample of the transformed data
print("\nSample of transformed data:")
key_columns = ['pickup_datetime', 'dropoff_datetime', 'trip_duration_mins']
# Only show columns that exist
display_columns = [col for col in key_columns if col in df.columns]
if len(display_columns) > 0:
    print(df[display_columns].head())

# Show additional columns if they exist
if 'pickup_date' in df.columns:
    print("\nTime-based columns sample:")
    time_columns = ['pickup_date', 'pickup_hour', 'pickup_day_of_week', 'pickup_month']
    display_time_columns = [col for col in time_columns if col in df.columns]
    print(df[display_time_columns].head())

print(f"\nTransformed data info:")
print(f"- Rows: {len(df)}")
print(f"- Columns: {len(df.columns)}")
print(f"- New columns added: {len(df.columns) - len(pd.read_csv(input_file, nrows=0).columns)}")

# Save transformed data
output_file = "../output/transformed_uber_data.csv"
try:
    df.to_csv(output_file, index=False)
    print(f"\n✅ SUCCESS: Saved transformed data to {output_file}")
    print(f"✅ File size: {os.path.getsize(output_file)} bytes")
except Exception as e:
    print(f"ERROR saving transformed data: {e}")
    exit()

print("\n🎉 data_transformation.py completed successfully!")