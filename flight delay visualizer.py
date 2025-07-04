import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Flight Delay Visualizer", layout="wide")
st.title("🛫 Flight Delay Visualizer Dashboard")

# -----------------------------
# 1. Load Dataset
# -----------------------------
@st.cache_data

def load_data():
    file_path = "flights_sample_3m.csv"  # Ensure this file is in your working dir
    df = pd.read_csv(file_path)
    df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], errors='coerce')
    delay_cols = ['DEP_DELAY', 'ARR_DELAY', 'DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER',
                  'DELAY_DUE_NAS', 'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT']
    for col in delay_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['IS_DELAYED'] = df['ARR_DELAY'] > 15
    df['MONTH'] = df['FL_DATE'].dt.to_period("M")
    return df

df = load_data()

# -----------------------------
# 2. Flight Volume by Carrier
# -----------------------------
st.subheader("✈️ Flight Volume by Carrier")
flight_volume = df['AIRLINE'].value_counts().reset_index()
flight_volume.columns = ['AIRLINE', 'FLIGHT_COUNT']
st.bar_chart(flight_volume.set_index('AIRLINE'))

# -----------------------------
# 3. Cancellation Reasons
# -----------------------------
st.subheader("❌ Cancellation Reasons")
cancel_map = {'A': 'Carrier', 'B': 'Weather', 'C': 'NAS', 'D': 'Security'}
df['CANCELLATION_REASON'] = df['CANCELLATION_CODE'].map(cancel_map)
cancel_counts = df['CANCELLATION_REASON'].value_counts()
st.bar_chart(cancel_counts)

# -----------------------------
# 4. Route Delay Heatmap
# -----------------------------
st.subheader("🌐 Route-wise Delay Heatmap")
route_delay = df.groupby(['ORIGIN', 'DEST'])['ARR_DELAY'].mean().reset_index()
pivot_delay = route_delay.pivot(index='ORIGIN', columns='DEST', values='ARR_DELAY')
pivot_delay = pivot_delay.dropna(thresh=10, axis=0).dropna(thresh=10, axis=1)
fig1, ax1 = plt.subplots(figsize=(14, 8))
sns.heatmap(pivot_delay, cmap='Reds', fmt=".1f", linewidths=0.5, cbar_kws={'label': 'Avg Arrival Delay (min)'}, ax=ax1)
ax1.set_title('Route-wise Average Arrival Delay')
st.pyplot(fig1)

# -----------------------------
# 5. Geo-Mapping
# -----------------------------
st.subheader("🗺️ Geo-Mapping of Average Arrival Delays")
airport_coords = {
    'DFW': (32.8998, -97.0403), 'SEA': (47.4502, -122.3088), 'SFO': (37.6213, -122.3790),
    'FLL': (26.0726, -80.1527), 'MSP': (44.8848, -93.2223), 'DEN': (39.8561, -104.6737),
    'MCO': (28.4312, -81.3081), 'DCA': (38.8512, -77.0402), 'BOS': (42.3656, -71.0096),
    'ORD': (41.9742, -87.9073), 'EWR': (40.6895, -74.1745), 'OKC': (35.3931, -97.6007),
    'DAL': (32.8471, -96.8517), 'HSV': (34.6372, -86.7751), 'SFB': (28.7776, -81.2375),
    'SWF': (41.5041, -74.1048), 'ATL': (33.6407, -84.4277), 'LAX': (33.9416, -118.4085),
    'PHX': (33.4342, -112.0116), 'LAS': (36.0840, -115.1537), 'JFK': (40.6413, -73.7781)
}

avg_delays = df.groupby('ORIGIN')['ARR_DELAY'].mean().reset_index()
avg_delays.columns = ['IATA', 'AvgDelay']
avg_delays['Latitude'] = avg_delays['IATA'].map(lambda x: airport_coords.get(x, (None, None))[0])
avg_delays['Longitude'] = avg_delays['IATA'].map(lambda x: airport_coords.get(x, (None, None))[1])
avg_delays = avg_delays.dropna(subset=['Latitude', 'Longitude'])
avg_delays['Size'] = avg_delays['AvgDelay'].clip(lower=0)

fig_geo = px.scatter_geo(
    avg_delays,
    lat='Latitude',
    lon='Longitude',
    color='AvgDelay',
    size='Size',
    hover_name='IATA',
    projection='natural earth',
    title='🛫 Avg Arrival Delays by Airport (Geo Map)',
    color_continuous_scale='RdBu_r'
)
fig_geo.update_layout(geo=dict(showland=True, landcolor="lightgray"))
st.plotly_chart(fig_geo, use_container_width=True)
