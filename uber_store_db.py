# uber_store_db.py
import pandas as pd
import sqlite3
import os
from datetime import datetime

print("Loading transformed data...")
# Load transformed data with proper settings
df = pd.read_csv("../output/transformed_uber_data.csv", low_memory=False)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print(f"Loaded {len(df)} rows")
print(f"Available columns: {list(df.columns)}")

# Create output directory if it doesn't exist
os.makedirs("../output", exist_ok=True)

# Connect to SQLite (easier than MySQL for local development)
db_path = "../output/uber_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Creating database table...")

# Create table based on available columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS uber_trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_datetime TEXT,
    pickup_date TEXT,
    pickup_hour INTEGER,
    pickup_day_of_week TEXT,
    pickup_month INTEGER,
    pick_up_address TEXT,
    pu_address TEXT,
    source_file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

print("Inserting data...")

# Prepare data for insertion (only columns that exist)
columns_to_insert = []
values_placeholders = []

# Check which columns exist in the dataframe
available_columns = {
    'pickup_datetime': 'pickup_datetime',
    'pickup_date': 'pickup_date', 
    'pickup_hour': 'pickup_hour',
    'pickup_day_of_week': 'pickup_day_of_week',
    'pickup_month': 'pickup_month',
    'pick_up_address': 'pick_up_address',
    'pu_address': 'pu_address',
    'source_file': 'source_file'
}

for db_col, df_col in available_columns.items():
    if df_col in df.columns:
        columns_to_insert.append(db_col)
        values_placeholders.append('?')

# Create insert statement
insert_sql = f"""
INSERT INTO uber_trips ({', '.join(columns_to_insert)})
VALUES ({', '.join(values_placeholders)})
"""

print(f"Insert statement: {insert_sql}")

# Insert data in batches for better performance
batch_size = 1000
total_inserted = 0

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    
    # Prepare batch data
    batch_data = []
    for _, row in batch.iterrows():
        row_data = []
        for _, df_col in available_columns.items():
            if df_col in df.columns:
                value = row[df_col]
                # Handle NaN values
                if pd.isna(value):
                    row_data.append(None)
                else:
                    row_data.append(value)
        batch_data.append(tuple(row_data))
    
    # Insert batch
    cursor.executemany(insert_sql, batch_data)
    total_inserted += len(batch_data)
    
    if i % 10000 == 0:  # Progress update every 10k rows
        print(f"Inserted {total_inserted} rows...")

# Commit changes
conn.commit()

# Verify insertion
cursor.execute("SELECT COUNT(*) FROM uber_trips")
count = cursor.fetchone()[0]

print(f"✅ Successfully stored {count} records in SQLite database!")
print(f"Database location: {os.path.abspath(db_path)}")

# Show sample data
print("\nSample data from database:")
cursor.execute("SELECT * FROM uber_trips LIMIT 5")
rows = cursor.fetchall()

# Get column names
cursor.execute("PRAGMA table_info(uber_trips)")
col_info = cursor.fetchall()
col_names = [row[1] for row in col_info]

print(f"Columns: {col_names}")
for i, row in enumerate(rows):
    print(f"Row {i+1}: {row}")

cursor.close()
conn.close()

print(f"\n✅ Data storage complete!")
print(f"You can now query your data using SQLite tools or Python.")