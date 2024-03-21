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

def create_criminal_profiling_dashboard():
    
    Criminal_Profiling = pd.read_csv('datasets/Criminal Profiling/Criminal_Profiling.csv')

    st.title("Criminal Profiling Dashboard")

    
    # Age Distribution
    st.subheader("Age Distribution")
    fig = px.histogram(Criminal_Profiling, x="age", nbins=20, title="Age Distribution of Criminals")
    st.plotly_chart(fig)


    # Gender Analysis
    st.subheader("Gender Analysis")
    gender_counts = Criminal_Profiling['Sex'].value_counts()
    fig = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, title="Gender Distribution")
    st.plotly_chart(fig)

    # Caste Analysis
    st.subheader("Caste Analysis")
    caste_counts = Criminal_Profiling[Criminal_Profiling['Caste'] != 'unknown']['Caste'].value_counts()
    fig = px.bar(x=caste_counts.index[:10], y=caste_counts.values[:10], title="Top 10 Caste Distribution based on Crimes", labels={'x': 'Caste', 'y': 'Count'})
    st.plotly_chart(fig)

    # Occupation Analysis
    st.subheader("Occupation Analysis")
    occupation_counts = Criminal_Profiling[(Criminal_Profiling['Occupation'] != "unknown") & (Criminal_Profiling['Occupation'] != "Others PI Specify")]['Occupation'].value_counts()
    occupation_counts = occupation_counts.sort_values(ascending=False)[:10]  # Sort in descending order
    fig = px.bar(x=occupation_counts.values[::-1], y=occupation_counts.index[::-1], orientation='h', title="Top 10 Occupation Associated with Criminal Activities", labels={'x': 'Count', 'y': 'Occupation'})
    st.plotly_chart(fig)


    # Top Crime Categories and Sub-Categories
    st.subheader("Top Crime Categories and Sub-Categories")
    top_crime_groups = Criminal_Profiling['Crime_Group1'].value_counts().nlargest(5)
    top_crime_heads = Criminal_Profiling['Crime_Head2'].value_counts().nlargest(5)
    
    tabs = st.tabs(["Category"," Sub- Category"])
    

    with tabs[0]:
        fig = px.bar(x=top_crime_groups.index, y=top_crime_groups.values, title="Top 5 Crime Groups Categories", labels={'x': 'Crime Group', 'y': 'Count'})
        st.plotly_chart(fig)

    with tabs[1]:
        fig = px.bar(x=top_crime_heads.index, y=top_crime_heads.values, title="Top 5 Crime Groups Sub-Categories", labels={'x': 'Crime Head', 'y': 'Count'})
        st.plotly_chart(fig)



if selected == "Home":
    st.write("Welcome to Predictive Guardians")

if selected == "Crime Pattern Analysis":

    @st.cache_data
    def load_data():
        # Get GeoJSON data
        url = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/states/karnataka.json"
        response = requests.get(url)
        geojson_data = response.json()
        crime_pattern_analysis = pd.read_csv("datasets/Crime Pattern Analysis/Crime_Pattern_Analysis_Cleaned.csv")
        mean_lat = crime_pattern_analysis['Latitude'].mean()
        mean_lon = crime_pattern_analysis['Longitude'].mean()
        return mean_lat,mean_lon, geojson_data, crime_pattern_analysis



    mean_lat, mean_lon, geojson_data, crime_pattern_analysis = load_data()

    # Title
    st.subheader("Temporal Analysis of Crime Data")

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
        else:  # Day
            data = filtered_df.groupby(["Day", "District_Name", "CrimeGroup_Name"]).size().reset_index(name="Count")
            fig = px.bar(data, x="Day", y="Count", color="District_Name", barmode="group", hover_data=["CrimeGroup_Name"])

        fig.update_layout(xaxis_title=selected_time_granularity, yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

   
    # st.subheader("Choropleth Maps")
    # chloropleth_maps(crime_pattern_analysis, geojson_data, mean_lat, mean_lon)

    # st.subheader("Heat Maps")
    # heatmap_type = st.selectbox("Choose Heatmap Type", ["Spatial Distribution of Crimes", 
    #                                                     "Temporal Distribution of Crimes by Year",
    #                                                     "Temporal Distribution of Crimes by Month"])
    
    # # Display the selected heat map
    # if heatmap_type == "Spatial Distribution of Crimes":
    #     heat_maps(crime_pattern_analysis, mean_lat, mean_lon, 'Latitude', 'Longitude', 'CrimeGroup_Name', 'Spatial Distribution of Crimes')
    # elif heatmap_type == "Temporal Distribution of Crimes by Year":
    #     heat_maps(crime_pattern_analysis, mean_lat, mean_lon, 'Latitude', 'Longitude', 'Year', 'Temporal Distribution of Crimes by Year')
    # elif heatmap_type == "Temporal Distribution of Crimes by Month":
    #     heat_maps(crime_pattern_analysis, mean_lat, mean_lon, 'Latitude', 'Longitude', 'Month', 'Temporal Distribution of Crimes by Month')

     
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
