import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
import folium
from folium import plugins
from sklearn.cluster import DBSCAN
import numpy as np
import requests
import plotly.io as pio
import streamlit.components.v1 as components


# Function to load and display HTML content
def display_html(file_path):
    with open(file_path, "r") as f:
        html_content = f.read()
    components.html(html_content, height=600)



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
    # Combine visualizations into a single dashboard
    with st.container():
        st.markdown("### Choropleth Maps")

        choropleth_metric = st.selectbox("Select Metric", ["Crime Incidents", "Victim Count", "Accused Count"], key="choropleth_metric")
        file_paths = {
            "Crime Incidents": "assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_FIRNo.html",
            "Victim Count": "assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_Victim.html",
            "Accused Count": "assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_Accused.html"
        }
        display_html(file_paths.get(choropleth_metric, ""))


    with st.container():
        st.markdown("### Heatmap")
        heatmap_metric = st.selectbox("Select Metric", ["Crimes", "Year", "Month"], key="heatmap_metric")

        file_paths = {
            "Crimes": "assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Crimes",
            "Year": "assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Year",
            "Month": "assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Month"
        }
        display_html(file_paths.get(heatmap_metric, ""))


    with st.container():
        st.markdown("### Cluster Analysis")
        folium_static(cluster_map)






