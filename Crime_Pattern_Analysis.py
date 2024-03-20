import numpy as np
import pandas as pd
import requests
import plotly.io as pio
import plotly.express as px
from sklearn.cluster import DBSCAN

df = pd.read_csv("datasets/Crime Pattern Analysis/Crime_Pattern_Analysis_Cleaned.csv")
mean_lat = df['Latitude'].mean()
mean_lon = df['Longitude'].mean()
# Get GeoJSON data
url = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/states/karnataka.json"
response = requests.get(url)
geojson_data = response.json()

def chloropleth_maps(df, mean_lat, mean_lon, geojson_data):
    # Group data by District_Name and aggregate by count of incidents, victim count, and accused count
    district_stats = df.groupby('District_Name').agg({'FIRNo': 'count', 'VICTIM COUNT': 'sum', 'Accused Count': 'sum'}).reset_index()

    # Create choropleth map based on crime rates
    fig1 = px.choropleth_mapbox(district_stats,
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

    # Create choropleth map based on victim counts
    fig2 = px.choropleth_mapbox(district_stats,
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

    # Create choropleth map based on accused counts
    fig3 = px.choropleth_mapbox(district_stats,
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

    
    # Save the figure as an HTML file
    pio.write_html(fig1, file="assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_FIRNo.html", auto_open=False, include_plotlyjs='cdn')
    pio.write_html(fig2, file="assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_Victim.html", auto_open=False, include_plotlyjs='cdn')
    pio.write_html(fig3, file="assets/Visualisations/Crime Pattern Analysis/Choropleth map/choropleth_map_Accused.html", auto_open=False, include_plotlyjs='cdn')


def heat_maps(df, mean_lat, mean_lon, lat_col, lon_col, color_col, title, save_path):
    fig = px.density_mapbox(df, lat=lat_col, lon=lon_col, z=color_col, radius=5,
                            center=dict(lat=mean_lat, lon=mean_lon),
                            zoom=10, mapbox_style="open-street-map",
                            title=title)
    fig.update_layout(margin=dict(r=0, l=0, t=0, b=0))
        
    # Save the figure as an HTML file
    pio.write_html(fig, file= save_path, auto_open=False, include_plotlyjs='cdn')



def cluster_analysis(df):
    # Select relevant features
    features = ['Latitude', 'Longitude', 'CrimeGroup_Name', 'CrimeHead_Name']
    crime_data = df[features]

    # Convert latitude and longitude to coordinates
    coords = crime_data[['Latitude', 'Longitude']].values

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=0.01, min_samples=10)
    clusters = dbscan.fit_predict(np.radians(coords))

    # Add cluster labels to the dataset
    crime_data['Cluster'] = clusters

    # Interactive Folium Map
    crime_map = folium.Map(location=[crime_data['Latitude'].mean(), crime_data['Longitude'].mean()], zoom_start=8)

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
    print("saving process started ...")
    crime_map.save("assets/Visualisations/Crime Pattern Analysis/Cluster analysis/Crime_clusters")


#chloropleth_maps(df, mean_lat, mean_lon, geojson_data)
#heat_maps(df, mean_lat, mean_lon, 'Latitude', 'Longitude', 'CrimeGroup_Name', 'Spatial Distribution of Crimes',"assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Crimes" )
#heat_maps(df, mean_lat, mean_lon, 'Latitude', 'Longitude', 'Year', 'Temporal Distribution of Crimes by Year',"assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Year" )
#heat_maps(df, mean_lat, mean_lon,'Latitude', 'Longitude', 'Month', 'Temporal Distribution of Crimes by Month',"assets/Visualisations/Crime Pattern Analysis/Heat map/Heat_map_Month" )

cluster_analysis(df)


