
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from sklearn.cluster import DBSCAN
from datetime import datetime
from streamlit_folium import folium_static
import plotly.express as px
import branca.colormap as cm


# Load your data
@st.cache_data
def load_data():
    # Replace this with your actual data loading code
    df = pd.read_csv('Component_datasets/Crime_Pattern_Analysis_Cleaned.csv')
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    return df

crime_pattern_analysis = load_data()

def aggregate_data(df):
    return df.groupby(['District_Name', 'UnitName', 'Latitude', 'Longitude', 'CrimeGroup_Name']).size().reset_index(name='Count')

def crime_hotspot_analysis(df, mean_lat, mean_lon):
    # Create base map
    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=8)

    # Create colormap
    colormap = cm.LinearColormap(colors=['blue', 'yellow', 'red'], vmin=0, vmax=df['Count'].max())

    # Add heatmap
    HeatMap(df[['Latitude', 'Longitude', 'Count']].values.tolist(), 
            gradient={0.4: 'blue', 0.65: 'yellow', 1: 'red'}, 
            radius=15).add_to(m)

    # Perform DBSCAN clustering
    coords = df[['Latitude', 'Longitude']].values
    dbscan = DBSCAN(eps=0.1, min_samples=5)
    df['Cluster'] = dbscan.fit_predict(coords)

    # Add markers for cluster centers
    for cluster in df['Cluster'].unique():
        if cluster != -1:  # -1 is noise in DBSCAN
            cluster_points = df[df['Cluster'] == cluster]
            center_lat = cluster_points['Latitude'].mean()
            center_lon = cluster_points['Longitude'].mean()
            count = cluster_points['Count'].sum()
            folium.Marker(
                [center_lat, center_lon],
                popup=f'Cluster {cluster}<br>Crimes: {count}',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

    # Add colormap legend to map
    colormap.add_to(m)
    colormap.caption = 'Crime Density'

    return m





def main():
    st.title("Crime Pattern Analysis")
    
    # Date range filter
    dates = st.radio("Select Date Range",["All","Custom Date Range"])

    if dates == "All":
        date_range = (crime_pattern_analysis['Date'].min(),crime_pattern_analysis['Date'].max())
    if dates == "Custom Date Range":
        date_range = st.date_input("Select date range", 
                                [crime_pattern_analysis['Date'].min(), crime_pattern_analysis['Date'].max()],
                                key='date_range')

    if len(date_range) != 2:
        st.stop()

    # Crime type filter
    crime_types = st.multiselect("Select crime types", crime_pattern_analysis['CrimeGroup_Name'].unique())

    if len(crime_types)==0:
        st.warning("Choose the desired Crime Groups from the above filters to see the map")
    

    # Filter data
    filtered_data = crime_pattern_analysis[
        (crime_pattern_analysis['Date'] >= pd.Timestamp(date_range[0])) & 
        (crime_pattern_analysis['Date'] <= pd.Timestamp(date_range[1]))
    ]
    if crime_types:
        filtered_data = filtered_data[filtered_data['CrimeGroup_Name'].isin(crime_types)]
    
    if st.button("Apply") and len(crime_types)!=0:
        # Aggregate data
        aggregated_data = aggregate_data(filtered_data)

        # Calculate mean lat and lon
        mean_lat = aggregated_data['Latitude'].mean()
        mean_lon = aggregated_data['Longitude'].mean()

        # Create and display maps
        st.subheader("Crime Hotspot Map")
        m = crime_hotspot_analysis(aggregated_data, mean_lat, mean_lon)
        folium_static(m)


        # Explanation
        st.markdown("""
        **How to interpret the maps:**
        - The heatmap shows the density of crimes. Red areas have more crimes.
        - Markers on the interactive map show the centers of high-crime clusters.
        - Use the date range and crime type filters to explore patterns over time and by crime category.
        - Zoom in for more detail in specific areas.
        - The density map provides a more granular view of crime concentration.
        """)

if __name__ == "__main__":
    main()
