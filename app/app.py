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
from Criminal_Profiling import create_criminal_profiling_dashboard
from Crime_Pattern_Analysis import *
from Predictive_modeling import *


with st.sidebar:
    selected = option_menu("Predictive Guardians", ['Home', 'Crime Pattern Analysis', "Criminal Profiling", 'Predictive Modeling', 'Resource Allocation and Guidance', 'Continuous Learning and Feedback', 'Documentation and Resources'], 
        icons=['house-fill', 'bar-chart-fill', "fingerprint", 'cpu-fill', 'diagram-3-fill', 'book-fill', 'file-earmark-text-fill' ], 
        menu_icon="shield-shaded", default_index=0, orientation="vertical",
        styles = {
        "container": {"padding": "5!important", "background-color": "#1c1e21"},
        "menu-title": {"font-size": "18px", "font-weight": "bold", "color": "#e5e5e5"},
        "menu-icon": {"color": "#62d0ff"},
        "nav": {"background-color": "#1c1e21"},
        "nav-item": {"padding": "0px 10px"},
        "nav-link": {
            "text-decoration": "none",
            "color": "#e5e5e5",
            "font-size": "14px",
            "font-weight": "normal",
            "--hover-color": "#62d0ff",
        },
        "nav-link-selected": {
            "background-color": "#62d0ff",
            "color": "#1c1e21",
            "font-weight": "bold",
        },
        "icon": {"color": "#e5e5e5", "font-size": "16px"},
        "separator": {"margin": "5px 0px", "border-color": "#343a40"},
    }
    )



if selected == "Home":
    st.write("Welcome to Predictive Guardians")

if selected == "Crime Pattern Analysis":

    @st.cache_data
    def load_data():
        # Get GeoJSON data
        url = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/states/karnataka.json"
        response = requests.get(url)
        geojson_data = response.json()
        crime_pattern_analysis = pd.read_csv("../datasets/Crime Pattern Analysis/Crime_Pattern_Analysis_Cleaned.csv")
        mean_lat = crime_pattern_analysis['Latitude'].mean()
        mean_lon = crime_pattern_analysis['Longitude'].mean()
        return mean_lat,mean_lon, geojson_data, crime_pattern_analysis



    mean_lat, mean_lon, geojson_data, crime_pattern_analysis = load_data()

    # Title
    st.subheader("Temporal Analysis of Crime Data")
    temporal_analysis(crime_pattern_analysis)

   
    st.subheader("Choropleth Maps")
    chloropleth_maps(crime_pattern_analysis, geojson_data, mean_lat, mean_lon)

    st.subheader("Heat Maps")
    heatmap_type = st.selectbox("Choose Heatmap Type", ["Spatial Distribution of Crimes", 
                                                        "Temporal Distribution of Crimes by Year",
                                                        "Temporal Distribution of Crimes by Month"])
    
    # Display the selected heat map
    if heatmap_type == "Spatial Distribution of Crimes":
        heat_maps(crime_pattern_analysis, mean_lat, mean_lon, 'Latitude', 'Longitude', 'CrimeGroup_Name', 'Spatial Distribution of Crimes')
    elif heatmap_type == "Temporal Distribution of Crimes by Year":
        heat_maps(crime_pattern_analysis, mean_lat, mean_lon, 'Latitude', 'Longitude', 'Year', 'Temporal Distribution of Crimes by Year')
    elif heatmap_type == "Temporal Distribution of Crimes by Month":
        heat_maps(crime_pattern_analysis, mean_lat, mean_lon, 'Latitude', 'Longitude', 'Month', 'Temporal Distribution of Crimes by Month')

     
    st.subheader("Cluster Analysis")
    crime_pattern_analysis = crime_pattern_analysis.reset_index(drop=True)

    # Randomly select 20% of observations from each unique combination of 'District_Name' and 'UnitName'
    sampled_data = crime_pattern_analysis.groupby(['District_Name', 'UnitName'], group_keys=False).apply(lambda x: x.sample(frac=0.01, random_state=1))

    # Reset the index of the sampled data
    sampled_data = sampled_data.reset_index(drop=True)
    mean_lat_sampled = sampled_data['Latitude'].mean()
    mean_lon_sampled = sampled_data['Longitude'].mean()
        
    cluster_analysis(sampled_data,mean_lat_sampled, mean_lon_sampled)




if selected == "Criminal Profiling":
    create_criminal_profiling_dashboard()


if selected == "Predictive Modeling":
    selected_component = st.radio("Select Prediction Component", ["Recidivism Prediction", "Crime Type Prediction", "Crime Hotspot Prediction"])

    # Display the selected component
    if selected_component == "Recidivism Prediction":
        predictive_modeling_recidivism()
    elif selected_component == "Crime Type Prediction":
        predictive_modeling_crime_type()
    elif selected_component == "Crime Hotspot Prediction":
        predictive_modeling_hotspot()

    

    