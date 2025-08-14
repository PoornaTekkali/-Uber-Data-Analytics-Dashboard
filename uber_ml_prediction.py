# uber_ml_prediction.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load and clean column names
df = pd.read_csv("../output/transformed_uber_data.csv", low_memory=False)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print(f"Total rows: {len(df)}")

# Check what's actually in these columns
cols = ['pickup_hour', 'pickup_day_of_week', 'trip_duration_mins']
for col in cols:
    if col in df.columns:
        print(f"\n{col}: {df[col].count()}/{len(df)} non-null")
        print(f"Sample values: {df[col].dropna().head(5).tolist()}")
    else:
        print(f"\n❌ {col} column missing!")

# Check ALL columns with data
print(f"\nColumns with actual data:")
for col in df.columns:
    count = len(df[col].dropna())
    if count > 0:
        print(f"  {col}: {count} values")

# Since we don't have trip duration, let's check what we can predict
print(f"\nLet's see what's in pickup_datetime:")
print(f"Sample pickup_datetime values: {df['pickup_datetime'].dropna().head(5).tolist()}")

# Instead of predicting trip duration, let's predict pickup_hour from day_of_week
# This is just a demo to show the model works
print(f"\n=== Creating Demo Model: Predict Time Period from Day of Week ===")

# Clean the data we do have
df['pickup_hour'] = pd.to_numeric(df['pickup_hour'], errors='coerce')
days_map = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
df['pickup_day_of_week'] = df['pickup_day_of_week'].astype(str).str.lower().map(days_map)

# Create a simple target: categorize hours into time periods
df['time_period'] = df['pickup_hour'].apply(lambda x: 
    0 if x < 6 else    # Early morning (0-5)
    1 if x < 12 else   # Morning (6-11)  
    2 if x < 18 else   # Afternoon (12-17)
    3)                 # Evening (18-23)

df_clean = df.dropna(subset=['pickup_hour', 'pickup_day_of_week'])
print(f"Clean data available: {len(df_clean)} rows")

if len(df_clean) > 0:
    # Train model to predict time period from day of week
    X = df_clean[['pickup_day_of_week']]
    y = df_clean['time_period']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"✅ Demo Model MAE: {mae:.3f} (predicting time period 0-3)")
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    # Show some predictions
    print(f"\nSample predictions:")
    for i in range(min(5, len(X_test))):
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        period_names = ['Early AM', 'Morning', 'Afternoon', 'Evening']
        day = int(X_test.iloc[i]['pickup_day_of_week'])
        actual_period = int(y_test.iloc[i])
        pred_period = int(round(y_pred[i]))
        print(f"  {day_names[day]} → Actual: {period_names[actual_period]}, Predicted: {period_names[pred_period]}")
else:
    print("❌ No valid data found. Check your CSV file!")