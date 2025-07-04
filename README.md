# ✈️ Flight Delay Visualizer Dashboard

## Overview
This project visualizes U.S. domestic flight delays using a real-world dataset (~1M rows). It enables interactive analysis of flight volumes, delays, cancellations, routes, and geospatial patterns to uncover the root causes and seasonal trends of delays.

## Objective
- Visualize flight delay trends, cancellations, and route-level performance.
- Identify carrier-specific and location-specific delay patterns.
- Explore spatial delay distributions via interactive geo maps.
- Build a foundation for future predictive models or alert systems.

## Dataset & Inputs
- U.S. domestic flight data (`flights_sample_3m.csv`) with ~1,000,000 rows (Source:- Kaggle https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023).
- Columns include date, carrier, delay causes, arrival/departure delays, origin/destination airports.

## Technologies Used
- Python, Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Streamlit (for interactive dashboard)

## How to Run

### Script Version
```bash
python flight_delay_visualizer.py
```

### Streamlit Dashboard Version
```bash
streamlit run flight_delay_visualizer.py
```

## Workflow
1. Data Cleaning & Type Conversion
2. Feature Engineering (`IS_DELAYED`, `MONTH`)
3. Visuals:
   - Flight Volume by Airline
   - Cancellation Reasons
   - Route Delay Heatmap (Origin vs. Destination)
   - Geo-Mapping of Avg Arrival Delays

## Visual Outputs
- Heatmap of delays by route
- Bar charts of airline volume & cancellation reasons
- Interactive geo scatter map of delays

## Key Takeaways
- Certain carriers and airports consistently show higher delays.
- Weather and carrier issues dominate cancellation reasons.
- Geo mapping highlights regional patterns in delays.

## Future Enhancements
- Add predictive delay modeling (e.g., RandomForest)
- Animate trends by month or season
- Enable multi-filter dashboard (carrier, route, month)
- Cluster airports based on delay profiles
