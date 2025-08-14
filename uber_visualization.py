# uber_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load transformed data from output folder
df = pd.read_csv("../output/transformed_uber_data.csv")

# Trips by hour
df['hour'] = pd.to_datetime(df['pickup_datetime']).dt.hour
plt.figure(figsize=(10, 6))
sns.countplot(x='hour', data=df, palette="viridis")
plt.title("Number of Trips by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Trip Count")
plt.savefig("../output/trips_by_hour.png")
plt.close()

# Trips by weekday
df['weekday'] = pd.to_datetime(df['pickup_datetime']).dt.day_name()
plt.figure(figsize=(10, 6))
sns.countplot(
    x='weekday',
    data=df,
    order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
plt.title("Number of Trips by Weekday")
plt.xlabel("Weekday")
plt.ylabel("Trip Count")
plt.savefig("../output/trips_by_weekday.png")
plt.close()

print("✅ Charts saved in output folder.")
