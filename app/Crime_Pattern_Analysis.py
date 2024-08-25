import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
import folium
from folium import plugins
from sklearn.cluster import DBSCAN
import numpy as np
import requests
import plotly.io as pio
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import folium_static
import pickle
from folium.plugins import HeatMap
from datetime import datetime
import branca.colormap as cm

def temporal_analysis(crime_pattern_analysis):

    # Instructions
    st.write(" ##### Instructions")
    st.write("1. Select the desired Districts and Crime Groups from the dropdown menus below.")
    st.write("2. After making your selection, click outside the dropdown menu or press the 'Esc' key to close the dropdown.")

    # Filters
    district_options = ["All Districts"] + sorted(crime_pattern_analysis["District_Name"].unique())
    selected_districts = st.multiselect("Select Districts", district_options, default=[])

    crime_group_options = ["All Crime Groups"] + sorted(crime_pattern_analysis["CrimeGroup_Name"].unique())
    selected_crime_groups = st.multiselect("Select Crime Groups", crime_group_options, default=[])

    selected_time_granularity = st.radio("Select Time Granularity", ["Year", "Month", "Day"])

    # Filter data based on selections
    if "All Districts" in selected_districts and "All Crime Groups" in selected_crime_groups:
        filtered_df = crime_pattern_analysis.copy()
    else:
        filtered_df = crime_pattern_analysis[
            (crime_pattern_analysis["District_Name"].isin(selected_districts) if selected_districts != ["All Districts"] else True) &
            (crime_pattern_analysis["CrimeGroup_Name"].isin(selected_crime_groups) if selected_crime_groups != ["All Crime Groups"] else True)
        ]

    # Temporal analysis visualizations
    if filtered_df.empty:
        st.warning("Choose the desired Districts and Crime Groups from the above filters")
    else:
        # Bar chart based on time granularity
        if selected_time_granularity == "Year":
            data = filtered_df.groupby(["Year", "District_Name", "CrimeGroup_Name"]).size().reset_index(name="Count")
            fig = px.bar(data, x="Year", y="Count", color="District_Name", barmode="group", hover_data=["CrimeGroup_Name"])
        elif selected_time_granularity == "Month":
            data = filtered_df.groupby(["Month", "District_Name", "CrimeGroup_Name"]).size().reset_index(name="Count")
            fig = px.bar(data, x="Month", y="Count", color="District_Name", barmode="group", hover_data=["CrimeGroup_Name"])
        elif selected_time_granularity == "Day":
            data = filtered_df.groupby(["Day", "District_Name", "CrimeGroup_Name"]).size().reset_index(name="Count")
            fig = px.bar(data, x="Day", y="Count", color="District_Name", barmode="group", hover_data=["CrimeGroup_Name"])

        fig.update_layout(xaxis_title=selected_time_granularity, yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)


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



def crime_hotspots(crime_pattern_analysis, mean_lat, mean_lon):
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
        aggregated_data = filtered_data.groupby(['District_Name', 'UnitName', 'Latitude', 'Longitude', 'CrimeGroup_Name']).size().reset_index(name='Count')

        # Calculate mean lat and lon
        mean_lat = aggregated_data['Latitude'].mean()
        mean_lon = aggregated_data['Longitude'].mean()

        # Create and display maps
        m = crime_hotspot_analysis(aggregated_data, mean_lat, mean_lon)
        folium_static(m)


        # Explanation
        st.markdown("""
        **How to interpret the map:**
        - The heatmap shows the density of crimes. Red areas have more crimes.
        - Markers on the interactive map show the centers of high-crime clusters.
        - Use the date range and crime type filters to explore patterns over time and by crime category.
        - Zoom in for more detail in specific areas.
        """)
 




def chloropleth_maps(df, geojson_data, mean_lat, mean_lon):
    # Group data by District_Name and aggregate by count of incidents, victim count, and accused count
    district_stats = df.groupby('District_Name').agg({'FIRNo': 'count', 'VICTIM COUNT': 'sum', 'Accused Count': 'sum'}).reset_index()

    # Choose the crime statistic to display
    selected_stat = st.selectbox('Select Crime Statistic', ['Crime Incidents', 'Total Victim Count', 'Total Accused Count'])

    # Create choropleth map based on the selected crime statistic
    if selected_stat == 'Crime Incidents':
        fig = px.choropleth_mapbox(district_stats,
                                   geojson=geojson_data,
                                   locations='District_Name',
                                   featureidkey="properties.district",
                                   color='FIRNo',
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=5,
                                   center={"lat": mean_lat, "lon": mean_lon},
                                   opacity=0.5,
                                   labels={'FIRNo': 'Crime Incidents'},
                                   title='Choropleth Map: Crime Incidents by District')
    elif selected_stat == 'Total Victim Count':
        fig = px.choropleth_mapbox(district_stats,
                                   geojson=geojson_data,
                                   locations='District_Name',
                                   featureidkey="properties.district",
                                   color='VICTIM COUNT',
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=5,
                                   center={"lat": mean_lat, "lon": mean_lon},
                                   opacity=0.5,
                                   labels={'VICTIM COUNT': 'Total Victim Count'},
                                   title='Choropleth Map: Total Victim Count by District')
    else:
        fig = px.choropleth_mapbox(district_stats,
                                   geojson=geojson_data,
                                   locations='District_Name',
                                   featureidkey="properties.district",
                                   color='Accused Count',
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=5,
                                   center={"lat": mean_lat, "lon": mean_lon},
                                   opacity=0.5,
                                   labels={'Accused Count': 'Total Accused Count'},
                                   title='Choropleth Map: Total Accused Count by District')

    # Display the choropleth map
    st.plotly_chart(fig) 
