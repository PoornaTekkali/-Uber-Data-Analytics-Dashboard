# Uber Data Analytics Project

## What This Project Does

This project takes Uber ride data from CSV files and turns it into useful insights. You can see patterns like when people ride most, which days are busiest, and get cool charts and an interactive dashboard.

## Why I Built This

I wanted to learn how to work with real data from start to finish. This project shows how to clean messy data, analyze it, and present it in a way that's easy to understand.

## What You Get

- Clean and organized data from messy CSV files
- Charts showing ride patterns by hour and day
- An interactive web dashboard you can filter and explore
- A database to store all the processed data
- Machine learning predictions for ride patterns

## Files in This Project

```
uber-analytics/
├── data/                     # Put your CSV files here
├── output/                   # Results go here
├── load_all_excel.py        # Combines all CSV files
├── data_cleaning.py         # Cleans up the data
├── data_transformation.py   # Creates new useful columns
├── data_analysis.py         # Finds patterns and insights
├── uber_dashboard.py        # Interactive web dashboard
├── uber_visualization.py    # Makes charts
├── uber_ml_prediction.py    # Machine learning predictions
├── uber_store_db.py         # Saves data to database
└── requirements.txt         # List of needed packages
```

## How to Use It

### Step 1: Get Ready
1. Download or clone this project
2. Install Python (version 3.7 or newer)
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Step 2: Add Your Data
- Put your Uber CSV files in the `data/` folder
- The CSV should have columns like DATE, TIME, pickup addresses

### Step 3: Run the Analysis
**IMPORTANT: You must run the data pipeline BEFORE starting the dashboard!**

**Easy way (Windows):**
```
run_pipeline.bat
```

**Step by step (Recommended):**
```
python load_all_excel.py      # Combine CSV files
python data_cleaning.py       # Clean the data
python data_transformation.py # Add useful columns
python data_analysis.py       # Analyze patterns
```

**Then start the dashboard:**
```
streamlit run uber_dashboard.py
```

Your browser will automatically open to http://localhost:8501

## Troubleshooting

### Dashboard Shows "Data file not found"
```
# Run these commands first:
python load_all_excel.py
python data_cleaning.py
python data_transformation.py

# Then start the dashboard:
streamlit run uber_dashboard.py
```

### "Module not found" errors
```
pip install -r requirements.txt
```

### Dashboard won't start
```
# Try a different port:
streamlit run uber_dashboard.py --server.port 8502
```

### Empty dashboard
- Make sure your CSV files are in the `data/` folder
- Check that the data pipeline ran successfully
- Look for any error messages in the terminal

### Step 4: See Your Results
- Open your browser to http://localhost:8501 (should open automatically)
- Charts will be saved in the `output/` folder
- Analysis results are printed in the terminal
- Use the dashboard to explore your data interactively

## Quick Start Checklist

✅ **Before running dashboard:**
1. Put CSV files in `data/` folder
2. Install requirements: `pip install -r requirements.txt`
3. Run data pipeline: `python load_all_excel.py` → `python data_cleaning.py` → `python data_transformation.py`
4. Start dashboard: `streamlit run uber_dashboard.py`

✅ **Your CSV files should have columns like:**
- DATE (any date format like 2023-01-15, 01/15/2023, etc.)
- TIME (like 14:30, 2:30 PM, etc.)
- Address columns (optional but helpful for maps)

## What You'll See

### Dashboard Features
- Total number of trips
- Busiest hours and days
- Interactive maps (if location data is available)
- Filters to explore specific time periods
- Charts that update as you filter

### Analysis Results
- Which hours have the most rides
- Busiest and quietest days of the week
- Trip duration patterns
- Data quality summary

## Problems This Solves

If you work with Uber or similar ride data, this helps you:
- Understand when demand is highest
- Plan driver schedules better
- See geographic patterns
- Make data-driven decisions
- Create reports for management

## What I Learned

Building this project taught me:
- How to handle messy real-world data
- Creating interactive dashboards
- Working with dates and times in data
- Building complete data pipelines
- Making data visualization that tells a story



## Things You Need to Know

### Your CSV Files Should Have:
- **DATE column** - Any format like 2023-01-15, 01/15/2023, Jan 15 2023
- **TIME column** - Any format like 14:30, 2:30 PM, 14:30:00
- **Address columns** - Optional but helpful for location analysis

### Common Issues and Fixes:

**"Data file not found" error:**
- You forgot to run the data pipeline first
- Run: `python load_all_excel.py` then `python data_cleaning.py` then `python data_transformation.py`

**"Module not found" error:**
- Missing required packages
- Run: `pip install -r requirements.txt`

**Dashboard is empty or broken:**
- Check that your CSV files are in the `data/` folder
- Make sure the CSV files have DATE and TIME columns
- Look for error messages in the terminal - they usually tell you what's wrong

**Dashboard won't start:**
- Port might be in use
- Try: `streamlit run uber_dashboard.py --server.port 8502`

### The project handles many problems automatically, but these are the most common issues.

## Future Ideas

Things I might add later:
- Weather data integration
- More advanced predictions
- Real-time data updates
- Mobile app version
- More chart types

## Tech Stack (What I Used)

- **Python** - Main programming language
- **Pandas** - For working with data
- **Streamlit** - For the web dashboard
- **Plotly** - For interactive charts
- **SQLite** - For storing data
- **Scikit-learn** - For machine learning

## Want to Contribute?

Feel free to:
- Report bugs or issues
- Suggest new features
- Improve the code
- Add more chart types
- Make the dashboard prettier

