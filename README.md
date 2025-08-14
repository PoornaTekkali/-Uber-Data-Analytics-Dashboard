🚖 Uber Data Analytics Project
📌 What This Project Does

This project takes raw Uber ride data and turns it into easy-to-read insights.
It shows patterns like:

When people take rides the most

Which days are the busiest

Interactive charts and dashboards you can explore

💡 Why I Built It

I wanted to learn how to work with real-world data from start to finish —
from cleaning messy files, to finding trends, and finally showing them in a way anyone can understand.

🛠 What’s Included

Clean data from messy CSV files

Charts & graphs showing ride patterns by hour and day

Interactive dashboard you can filter and explore

Database storage for processed data

Machine learning predictions for ride patterns

📂 Project Structure
uber-analytics/
├── data/                     # Raw Uber CSV files
├── output/                   # Processed data & charts
├── load_all_excel.py         # Combines CSV files
├── data_cleaning.py          # Cleans the data
├── data_transformation.py    # Adds new useful columns
├── data_analysis.py          # Finds patterns
├── uber_dashboard.py         # Interactive dashboard
├── uber_visualization.py     # Creates charts
├── uber_ml_prediction.py     # Makes predictions
├── uber_store_db.py          # Saves data to a database
└── requirements.txt          # List of Python packages needed

🚀 How to Run It
Step 1: Install Requirements

Download or clone this project

Install Python (3.7 or newer)

Install needed packages:

pip install -r requirements.txt

Step 2: Add Your Data

Put your Uber CSV files in the data/ folder

They should have at least:

DATE column (any format)

TIME column (any format)

Step 3: Process the Data

Run the scripts in this order:

python load_all_excel.py
python data_cleaning.py
python data_transformation.py

Step 4: Start the Dashboard
streamlit run uber_dashboard.py


Your browser will open at http://localhost:8501.

🧠 What You’ll See in the Dashboard

Total rides

Most popular hours & days

Interactive maps (if location data is available)

Filters for exploring certain dates or times

Charts that change based on your filters

🛠 Common Issues & Fixes

"Data file not found" → Run the data scripts first.

"Module not found" → Install packages:

pip install -r requirements.txt


Dashboard is empty → Check your CSV is in data/ and has DATE/TIME columns.

Dashboard won’t start → Try another port:

streamlit run uber_dashboard.py --server.port 8502

🌱 Future Improvements

Add weather data

Real-time updates

Mobile-friendly dashboard

More advanced predictions

🧰 Tech Stack

Python

Pandas

Streamlit

Plotly

SQLite

Scikit-learn
