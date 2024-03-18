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
        if choropleth_metric == "Crime Incidents":
            # Load the HTML file
            with open("assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_FIRNo.html", "r") as f:
                html_content = f.read()

            # Render the HTML content in Streamlit
            components.html(html_content, height=600)

        elif choropleth_metric == "Victim Count":
            # Load the HTML file
            with open("assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_Victim.html", "r") as f:
                html_content = f.read()

            # Render the HTML content in Streamlit
            components.html(html_content, height=600)

        else:
            # Load the HTML file
            with open("assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_Accused.html", "r") as f:
                html_content = f.read()

            # Render the HTML content in Streamlit
            components.html(html_content, height=600)



    with st.container():
        st.markdown("### Heatmap")
        heatmap_metric = st.selectbox("Select Metric", ["Crimes", "Year", "Month"], key="heatmap_metric")

        if heatmap_metric == "Crimes":
            # Load the HTML file
            with open("assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Crimes", "r") as f:
                html_content = f.read()
            # Render the HTML content in Streamlit
            components.html(html_content, height=600)

        if heatmap_metric == "Year":
            # Load the HTML file
            with open("assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Year", "r") as f:
                html_content = f.read()
            # Render the HTML content in Streamlit
            components.html(html_content, height=600)

        if heatmap_metric == "Month":
            # Load the HTML file
            with open("assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Month", "r") as f:
                html_content = f.read()
            # Render the HTML content in Streamlit
            components.html(html_content, height=600)







# # Select relevant features
# features = ['Latitude', 'Longitude', 'CrimeGroup_Name', 'CrimeHead_Name']
# crime_data = crime_data[features]

# # Handle missing values if any
# crime_data = crime_data.dropna(subset=features)

# # Convert latitude and longitude to coordinates
# coords = crime_data[['Latitude', 'Longitude']].values

# # Perform DBSCAN clustering
# dbscan = DBSCAN(eps=0.01, min_samples=10)
# clusters = dbscan.fit_predict(np.radians(coords))

# # Add cluster labels to the dataset
# crime_data['Cluster'] = clusters

# # Interactive Folium Map
# crime_map = folium.Map(location=[crime_data['Latitude'].mean(), crime_data['Longitude'].mean()], zoom_start=8)

# # Add markers for each crime incident, colored by cluster
# for idx, row in crime_data.iterrows():
#     folium.CircleMarker(
#         location=[row['Latitude'], row['Longitude']],
#         radius=5,
#         color='red' if row['Cluster'] == -1 else 'green',
#         fill=True,
#         fill_color='red' if row['Cluster'] == -1 else 'green',
#         fill_opacity=0.6,
#         tooltip=f"Cluster: {row['Cluster']}<br>Crime Group: {row['CrimeGroup_Name']}<br>Crime Head: {row['CrimeHead_Name']}"
#     ).add_to(crime_map)

# # Add a heatmap layer
# crimes = crime_data[['Latitude', 'Longitude']].values.tolist()
# heatmap = plugins.HeatMap(crimes, radius=15)
# crime_map.add_child(heatmap)

# # Display the Folium map
# crime_map
