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
from Resource_Allocation import *
from Continuous_Learning_and_Feedback import *
import os


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with st.sidebar:
    selected = option_menu("Predictive Guardians", ['Home', 'Crime Pattern Analysis', "Criminal Profiling", 'Predictive Modeling', 'Police Resource Allocation and Management', 'Continuous Learning and Feedback', 'Documentation and Resources'], 
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
    st.title("Welcome to Predictive Guardians 🚔💻")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            Predictive Guardians is an innovative, AI-powered solution that revolutionizes the way law enforcement agencies approach public safety. By utilizing advanced data analysis and machine learning, my platform empowers agencies to make data-driven decisions, enabling them to allocate resources more efficiently and effectively.
            """
        )
        st.markdown(
            """
            Predictive Guardians provides law enforcement agencies with the insights and actionable intelligence they need to stay one step ahead of criminals. My solution covers a comprehensive suite of analytical tools, including:
            """
        )
        st.markdown(
            """
            - **Crime Pattern Analysis**: Uncover hidden insights and trends through spatial, temporal, and cluster-based analysis.
            - **Criminal Profiling**: Develop targeted crime prevention strategies by understanding the characteristics and behavioral patterns of offenders.
            - **Predictive Modeling**: Forecast future crime trends and patterns, enabling proactive resource allocation and intervention.
            - **Resource Allocation**: Optimize the deployment of police personnel to ensure efficient and effective utilization of law enforcement resources.
            - **Continuous Learning and Feedback**: Facilitate ongoing system improvement by incorporating user feedbacks, alerts, organizing collaborative learning sessions, and maintaining a knowledge base to document insights and lessons learned.
            """
        )
        st.markdown(
            """
            Join me on this transformative journey as we redefine the future of public safety and ensure that our communities are safe, secure, and resilient. With Predictive Guardians, the path to a safer tomorrow is within reach.
            """
        )
        if st.button("Learn More"):
            st.session_state.selected_page = "Documentation and Resources"
            st.experimental_rerun()

    with col2:
        data_file_path = os.path.join(root_dir, 'assets', 'Home_Page_image.jpg')
        st.image(data_file_path, use_container_width=True)


if st.session_state.get("selected_page", "Home") == "Documentation and Resources":
    st.markdown('Click [here](https://github.com/VishalKumar-S/Predictive_Guardians/blob/main/Readme.md) to view the documentation and resources.')


if selected == "Crime Pattern Analysis":

    @st.cache_data
    def load_data():
        # Get GeoJSON data of all district co-ordinates of Karnataka
        url = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/states/karnataka.json"
        response = requests.get(url)
        geojson_data = response.json()
        data_file_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Pattern_Analysis_Cleaned.csv')

        crime_pattern_analysis = pd.read_csv(data_file_path)
        mean_lat = crime_pattern_analysis['Latitude'].mean()
        mean_lon = crime_pattern_analysis['Longitude'].mean()
        return mean_lat,mean_lon, geojson_data, crime_pattern_analysis



    mean_lat, mean_lon, geojson_data, crime_pattern_analysis = load_data()


    st.subheader("Temporal Analysis of Crime Data")
    temporal_analysis(crime_pattern_analysis)

   
    st.subheader("Choropleth Maps")
    chloropleth_maps(crime_pattern_analysis, geojson_data, mean_lat, mean_lon)
    


    st.subheader("Crime Hotspot Map")
    crime_pattern_analysis = crime_pattern_analysis.reset_index(drop=True)


    mean_lat_sampled = crime_pattern_analysis['Latitude'].mean()
    mean_lon_sampled = crime_pattern_analysis['Longitude'].mean()
    crime_pattern_analysis['Date'] = pd.to_datetime(crime_pattern_analysis[['Year', 'Month', 'Day']])
    crime_hotspots(crime_pattern_analysis,mean_lat_sampled, mean_lon_sampled)




if selected == "Criminal Profiling":
    create_criminal_profiling_dashboard()


if selected == "Predictive Modeling":
    # selected_component = st.radio("Select Prediction Component", ["Repeat Offense Prediction", "Crime Type Prediction"])

    # Display the selected component
    #if selected_component == "Repeat Offense Prediction":
    predictive_modeling_recidivism()
    # elif selected_component == "Crime Type Prediction":
    #     predictive_modeling_crime_type()



if selected == "Police Resource Allocation and Management":    
    # Construct the file path
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Resource_Allocation_Cleaned.csv')
    
    # Read the data
    df = pd.read_csv(data_file_path)
    resource_allocation(df)

if selected == "Continuous Learning and Feedback":
    continuous_learning_and_feedback()

if selected == "Documentation and Resources":
    st.markdown('You selected "Documentation and Resources". Click [here](https://github.com/VishalKumar-S/Predictive_Guardians/blob/main/Readme.md) to view the documentation and resources.')



    

    
