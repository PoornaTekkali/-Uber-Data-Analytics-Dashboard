import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Uber Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4ECDC4;
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the data"""
    try:
        df = pd.read_csv("../output/transformed_uber_data.csv")
        
        # Handle duplicate columns with a simpler approach
        cols = df.columns.tolist()
        seen = {}
        for i, col in enumerate(cols):
            if col in seen:
                seen[col] += 1
                cols[i] = f"{col}_{seen[col]}"
            else:
                seen[col] = 0
        df.columns = cols
        
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'transformed_uber_data.csv' exists in the output folder.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data
df = load_data()

if df.empty:
    st.stop()

# Main title
st.markdown('<h1 class="main-header">🚗 Uber Data Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("### 🎛️ Dashboard Filters")

# Ride type filter
ride_types = df['ride_type'].unique() if 'ride_type' in df.columns else ['All']
selected_ride = st.sidebar.multiselect(
    "🚙 Select Ride Type", 
    ride_types, 
    default=ride_types,
    help="Filter trips by ride type"
)

# Time filters
col1, col2 = st.sidebar.columns(2)
with col1:
    start_hour = st.slider("Start Hour", 0, 23, 0)
with col2:
    end_hour = st.slider("End Hour", 0, 23, 23)

# Date range filter (if date columns exist)
if 'pickup_date' in df.columns:
    df['pickup_date'] = pd.to_datetime(df['pickup_date'], errors='coerce')
    date_range = st.sidebar.date_input(
        "📅 Select Date Range",
        value=(df['pickup_date'].min(), df['pickup_date'].max()),
        min_value=df['pickup_date'].min(),
        max_value=df['pickup_date'].max()
    )

# Apply filters
filtered_df = df.copy()

if 'ride_type' in df.columns and selected_ride:
    filtered_df = filtered_df[filtered_df['ride_type'].isin(selected_ride)]

if 'pickup_hour' in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df['pickup_hour'] >= start_hour) & 
        (filtered_df['pickup_hour'] <= end_hour)
    ]

# Key Metrics Row
st.markdown("## 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_trips = len(filtered_df)
    st.metric("Total Trips", f"{total_trips:,}", delta=None)

with col2:
    if 'trip_duration_mins' in filtered_df.columns:
        avg_duration = filtered_df['trip_duration_mins'].mean()
        st.metric("Avg Duration", f"{avg_duration:.1f} min", delta=None)
    else:
        st.metric("Avg Duration", "N/A", delta=None)

with col3:
    if 'fare_amount' in filtered_df.columns:
        total_revenue = filtered_df['fare_amount'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}", delta=None)
    else:
        st.metric("Total Revenue", "N/A", delta=None)

with col4:
    peak_hour = filtered_df.groupby('pickup_hour').size().idxmax() if 'pickup_hour' in filtered_df.columns else "N/A"
    st.metric("Peak Hour", f"{peak_hour}:00" if peak_hour != "N/A" else "N/A", delta=None)

st.divider()

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    # Enhanced Trips by Hour
    if 'pickup_hour' in filtered_df.columns:
        st.markdown("### 🕐 Trips by Hour")
        trips_by_hour = filtered_df.groupby('pickup_hour').size().reset_index(name='trip_count')
        
        fig_hour = px.bar(
            trips_by_hour, 
            x='pickup_hour', 
            y='trip_count',
            title="Hourly Trip Distribution",
            color='trip_count',
            color_continuous_scale='viridis'
        )
        fig_hour.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Number of Trips",
            showlegend=False
        )
        st.plotly_chart(fig_hour, use_container_width=True)

with col2:
    # Enhanced Trips by Weekday
    if 'pickup_day_of_week' in filtered_df.columns:
        st.markdown("### 📅 Trips by Weekday")
        trips_by_weekday = filtered_df.groupby('pickup_day_of_week').size().reset_index(name='trip_count')
        
        # Map day numbers to names
        day_names = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        trips_by_weekday['day_name'] = trips_by_weekday['pickup_day_of_week'].map(day_names)
        
        fig_weekday = px.bar(
            trips_by_weekday, 
            x='day_name', 
            y='trip_count',
            title="Weekly Trip Distribution",
            color='trip_count',
            color_continuous_scale='plasma'
        )
        fig_weekday.update_layout(
            xaxis_title="Day of Week",
            yaxis_title="Number of Trips",
            showlegend=False
        )
        st.plotly_chart(fig_weekday, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    # Trip Duration Distribution
    if 'trip_duration_mins' in filtered_df.columns:
        st.markdown("### ⏱️ Trip Duration Distribution")
        
        # Remove outliers for better visualization
        q95 = filtered_df['trip_duration_mins'].quantile(0.95)
        duration_filtered = filtered_df[filtered_df['trip_duration_mins'] <= q95]
        
        fig_duration = px.histogram(
            duration_filtered, 
            x='trip_duration_mins', 
            nbins=30,
            title="Trip Duration Distribution (95th percentile)",
            color_discrete_sequence=['#FF6B6B']
        )
        fig_duration.update_layout(
            xaxis_title="Duration (minutes)",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig_duration, use_container_width=True)

with col2:
    # Ride Type Distribution (if available)
    if 'ride_type' in filtered_df.columns:
        st.markdown("### 🚗 Ride Type Distribution")
        ride_type_counts = filtered_df['ride_type'].value_counts()
        
        fig_pie = px.pie(
            values=ride_type_counts.values,
            names=ride_type_counts.index,
            title="Distribution by Ride Type"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# Map Visualization (Full Width)
if 'start_lat' in filtered_df.columns and 'start_lng' in filtered_df.columns:
    st.markdown("### 🗺️ Trip Locations")
    
    # Sample data for better performance
    if len(filtered_df) > 1000:
        map_df = filtered_df.sample(n=1000)
        st.info("Showing a random sample of 1000 trips for better map performance")
    else:
        map_df = filtered_df
    
    # Remove invalid coordinates
    map_df = map_df.dropna(subset=['start_lat', 'start_lng'])
    map_df = map_df[
        (map_df['start_lat'].between(-90, 90)) & 
        (map_df['start_lng'].between(-180, 180))
    ]
    
    if not map_df.empty:
        fig_map = px.scatter_mapbox(
            map_df, 
            lat='start_lat', 
            lon='start_lng',
            color='trip_duration_mins' if 'trip_duration_mins' in map_df.columns else None,
            size='trip_duration_mins' if 'trip_duration_mins' in map_df.columns else None,
            color_continuous_scale='viridis',
            size_max=15, 
            zoom=10,
            title="Trip Pickup Locations",
            hover_data={'trip_duration_mins': True} if 'trip_duration_mins' in map_df.columns else None
        )
        fig_map.update_layout(
            mapbox_style="open-street-map",
            height=500
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No valid coordinate data available for map visualization")

# Advanced Analytics Section
st.markdown("## 📈 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    # Correlation heatmap (if numeric columns exist)
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        st.markdown("### 🔥 Correlation Matrix")
        corr_matrix = filtered_df[numeric_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            title="Feature Correlation Heatmap",
            aspect="auto",
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

with col2:
    # Trip statistics by ride type
    if 'ride_type' in filtered_df.columns and 'trip_duration_mins' in filtered_df.columns:
        st.markdown("### 📊 Statistics by Ride Type")
        stats_df = filtered_df.groupby('ride_type')['trip_duration_mins'].agg([
            'count', 'mean', 'median', 'std'
        ]).round(2)
        stats_df.columns = ['Count', 'Mean Duration', 'Median Duration', 'Std Dev']
        st.dataframe(stats_df, use_container_width=True)

# Data Export Section
st.markdown("## 💾 Data Export")
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Download Filtered Data", type="primary"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_uber_data.csv",
            mime="text/csv"
        )

with col2:
    st.info(f"Current dataset contains {len(filtered_df)} trips after applying filters")

# Sample Data Display
with st.expander("🔍 View Sample Data", expanded=False):
    st.dataframe(
        filtered_df.head(100), 
        use_container_width=True,
        height=400
    )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888888;'>"
    "Built with ❤️ using Streamlit | Data Analytics Dashboard"
    "</div>", 
    unsafe_allow_html=True
)