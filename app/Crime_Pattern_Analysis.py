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


def temporal_analysis(crime_pattern_analysis):


    
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



def cluster_analysis(sampled_data,mean_lat, mean_lon):
    # Select relevant features
    features = ['Latitude', 'Longitude', 'CrimeGroup_Name', 'CrimeHead_Name']
    crime_data = sampled_data[features]                     


    # Convert latitude and longitude to coordinates
    coords = crime_data[['Latitude', 'Longitude']].values

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=0.01, min_samples=10)
    clusters = dbscan.fit_predict(np.radians(coords))

    # Add cluster labels to the dataset
    crime_data['Cluster'] = clusters

    # Interactive Folium Map
    crime_map = folium.Map(location=[mean_lat, mean_lon], zoom_start=8)

    # Add markers for each crime incident, colored by cluster
    for idx, row in crime_data.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color='red' if row['Cluster'] == -1 else 'green',
            fill=True,
            fill_color='red' if row['Cluster'] == -1 else 'green',
            fill_opacity=0.6,
            tooltip=f"Cluster: {row['Cluster']}<br>Crime Group: {row['CrimeGroup_Name']}<br>Crime Head: {row['CrimeHead_Name']}"
        ).add_to(crime_map)

    # Add a heatmap layer
    crimes = crime_data[['Latitude', 'Longitude']].values.tolist()
    heatmap = plugins.HeatMap(crimes, radius=15)
    crime_map.add_child(heatmap)

    folium_static(crime_map)

    #Cluster Statistics
    st.write("Cluster Statistics")
    cluster_stats = crime_data.groupby(['Cluster', 'CrimeGroup_Name'])['CrimeHead_Name'].count().reset_index()
    fig = px.bar(cluster_stats, x='CrimeGroup_Name', y='CrimeHead_Name', color='Cluster', barmode='group', title='Distribution of Crime Types within Clusters')
    # Display Plotly figure
    st.plotly_chart(fig)

def heat_maps(df, mean_lat, mean_lon, lat_col, lon_col, color_col, title):
    fig = px.density_mapbox(df, lat=lat_col, lon=lon_col, z=color_col, radius=5,
                            center=dict(lat=mean_lat, lon=mean_lon),
                            zoom=10, mapbox_style="open-street-map",
                            title=title)
    fig.update_layout(margin=dict(r=0, l=0, t=0, b=0))
    st.plotly_chart(fig)

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
