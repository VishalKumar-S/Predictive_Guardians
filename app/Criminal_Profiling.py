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

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))



# Read the data
df = pd.read_csv(data_file_path)


def create_criminal_profiling_dashboard():

    # Construct the file path
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Criminal_Profiling_cleaned.csv')
    
    Criminal_Profiling = pd.read_csv(data_file_path)

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
        fig = px.bar(x=top_crime_groups.index, y=top_crime_groups.values, title="Top 5 Most Frequent Crime Group Categories", labels={'x': 'Crime Group', 'y': 'Count'})
        st.plotly_chart(fig)

    with tabs[1]:
        fig = px.bar(x=top_crime_heads.index, y=top_crime_heads.values, title="Top 5 Crime Groups Sub-Categories", labels={'x': 'Crime Head', 'y': 'Count'})
        st.plotly_chart(fig)


