import pandas as pd
import os

print("Starting data_analysis.py...")

# Check if transformed data exists
input_file = "../output/transformed_uber_data.csv"
if not os.path.exists(input_file):
    print(f"ERROR: {input_file} not found!")
    print("Please run data_transformation.py first to create the transformed data file.")
    exit()

# Load transformed data
print(f"Loading data from {input_file}...")
try:
    df = pd.read_csv(input_file, low_memory=False)
    print(f"✅ Loaded data with shape: {df.shape}")
    print(f"✅ Columns available: {df.columns.tolist()}")
except Exception as e:
    print(f"ERROR loading data: {e}")
    exit()

print("\n" + "="*60)
print("🚗 UBER DATA ANALYSIS RESULTS")
print("="*60)

# ANALYSIS 1: Basic Data Overview
print("\n📊 ANALYSIS 1: Data Overview")
print("-" * 30)
print(f"Total rides in dataset: {len(df):,}")
print(f"Total columns: {len(df.columns)}")

# Show data sample
print("\nData sample:")
print(df.head())

# ANALYSIS 2: Rides per day analysis
if 'pickup_datetime' in df.columns:
    print("\n📅 ANALYSIS 2: Daily Ride Patterns")
    print("-" * 30)
    
    # Convert to datetime
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
    
    # Check how many valid datetime entries we have
    valid_datetimes = df['pickup_datetime'].notna().sum()
    print(f"Valid pickup_datetime entries: {valid_datetimes:,} out of {len(df):,}")
    
    if valid_datetimes > 0:
        # Create date column
        df['date'] = df['pickup_datetime'].dt.date
        rides_per_day = df.groupby('date').size().sort_index()
        
        print(f"\nDaily ride statistics:")
        print(f"- Total days with data: {len(rides_per_day)}")
        print(f"- Average rides per day: {rides_per_day.mean():.1f}")
        print(f"- Maximum rides in a day: {rides_per_day.max()}")
        print(f"- Minimum rides in a day: {rides_per_day.min()}")
        
        print(f"\nFirst 10 days with ride counts:")
        print(rides_per_day.head(10))
        
        print(f"\nLast 10 days with ride counts:")
        print(rides_per_day.tail(10))
    else:
        print("❌ No valid pickup_datetime data available for daily analysis")
else:
    print("\n❌ ANALYSIS 2: No pickup_datetime column found")

# ANALYSIS 3: Hourly patterns (if we have hour data)
if 'pickup_hour' in df.columns:
    print("\n🕐 ANALYSIS 3: Hourly Ride Patterns")
    print("-" * 30)
    
    hourly_rides = df['pickup_hour'].value_counts().sort_index()
    print("Rides by hour of day:")
    for hour, count in hourly_rides.items():
        if not pd.isna(hour):
            print(f"  {int(hour):02d}:00 - {count:,} rides")
    
    busiest_hour = hourly_rides.idxmax()
    quietest_hour = hourly_rides.idxmin()
    print(f"\nBusiest hour: {int(busiest_hour):02d}:00 ({hourly_rides.max():,} rides)")
    print(f"Quietest hour: {int(quietest_hour):02d}:00 ({hourly_rides.min():,} rides)")

# ANALYSIS 4: Day of week patterns
if 'pickup_day_of_week' in df.columns:
    print("\n📆 ANALYSIS 4: Day of Week Patterns")
    print("-" * 30)
    
    daily_rides = df['pickup_day_of_week'].value_counts()
    
    # Order days properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_rides_ordered = daily_rides.reindex([day for day in day_order if day in daily_rides.index])
    
    print("Rides by day of week:")
    for day, count in daily_rides_ordered.items():
        print(f"  {day}: {count:,} rides")
    
    busiest_day = daily_rides.idxmax()
    quietest_day = daily_rides.idxmin()
    print(f"\nBusiest day: {busiest_day} ({daily_rides.max():,} rides)")
    print(f"Quietest day: {quietest_day} ({daily_rides.min():,} rides)")

# ANALYSIS 5: Trip duration stats (if available)
if 'trip_duration_mins' in df.columns:
    print("\n⏱️  ANALYSIS 5: Trip Duration Analysis")
    print("-" * 30)
    
    # Count non-null trip durations
    non_null_duration = df['trip_duration_mins'].notna().sum()
    if non_null_duration > 0:
        print(f"Available trip duration data: {non_null_duration:,} rides")
        print("\nTrip duration statistics (minutes):")
        print(df['trip_duration_mins'].describe())
    else:
        print("❌ No trip duration data available (all values are null)")
else:
    print("\n❌ ANALYSIS 5: No trip_duration_mins column found")

# ANALYSIS 6: Data source analysis
if 'source_file' in df.columns:
    print("\n📁 ANALYSIS 6: Data Source Breakdown")
    print("-" * 30)
    
    rides_by_source = df['source_file'].value_counts()
    print(f"Data from {len(rides_by_source)} different files:")
    
    for i, (source, count) in enumerate(rides_by_source.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"  {i}. {source}: {count:,} rides ({percentage:.1f}%)")
    
    print(f"\nLargest file: {rides_by_source.index[0]} ({rides_by_source.iloc[0]:,} rides)")
    print(f"Smallest file: {rides_by_source.index[-1]} ({rides_by_source.iloc[-1]:,} rides)")
else:
    print("\n❌ ANALYSIS 6: No source_file information available")

# ANALYSIS 7: Data Quality Summary
print("\n🔍 ANALYSIS 7: Data Quality Summary")
print("-" * 30)

print(f"Dataset overview:")
print(f"- Total rows: {len(df):,}")
print(f"- Total columns: {len(df.columns)}")

# Check for missing values in key columns
key_columns = ['pickup_datetime', 'source_file', 'pickup_hour', 'pickup_day_of_week']
print(f"\nMissing value analysis:")
for col in key_columns:
    if col in df.columns:
        missing = df[col].isna().sum()
        missing_pct = (missing / len(df)) * 100
        print(f"- {col}: {missing:,} missing ({missing_pct:.1f}%)")

# Memory usage
memory_usage_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
print(f"\nMemory usage: {memory_usage_mb:.1f} MB")

print("\n" + "="*60)
print("✅ DATA ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*60)

print("\n🎉 data_analysis.py completed successfully!")