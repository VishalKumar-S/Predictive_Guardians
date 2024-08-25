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
import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import folium
from folium.plugins import HeatMap, Fullscreen
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import calinski_harabasz_score
import os
import joblib
import json



# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@st.cache_data
def load_data_recidivism():
    # Construct the file path
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Recidivism_cleaned_data.csv')
    return pd.read_csv(data_file_path)


# Load the model
@st.cache_resource
def load_model_recidivism():
    model_file_path = os.path.join(root_dir, 'models', 'Recidivism_model', 'StackedEnsemble_BestOfFamily_2_AutoML_1_20240719_183320.zip')
    saved_model = h2o.import_mojo(model_file_path)
    return saved_model

@st.cache_data
def load_data_crime_type():
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Type_cleaned_data.csv')
    return pd.read_csv(data_file_path)

@st.cache_data
def load_data_hotspot():
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Hotspot_Cleaned.csv')
    return pd.read_csv(data_file_path)

# Load the model
@st.cache_resource
def load_model_crime_type():
    model_file_path = os.path.join(root_dir, 'models', 'Crime_Type_Prediction', 'GBM_1_AutoML_2_20240521_83242.zip')
    saved_model = h2o.import_mojo(model_file_path)
    return saved_model

def get_unique_values(data, feature):
    return data[feature].unique().tolist()

def get_unique_values_crime_type(data, feature):
    return data[feature].unique().tolist()





def predictive_modeling_recidivism():
    st.subheader("Repeat Offense Prediction App")
    st.write("Predict whether a previous accused, will again commit a crime or not")

    h2o.init()
    # Load the model
    model = load_model_recidivism()

    scaler = joblib.load('../models/Recidivism_model/scaler.pkl')

    cleaned_data = load_data_recidivism()
    # Get unique values for categorical features
    unique_castes = get_unique_values(cleaned_data, 'Caste')
    unique_professions = get_unique_values(cleaned_data, 'Profession')
    unique_districts = get_unique_values(cleaned_data, 'District_Name')
    unique_cities = get_unique_values(cleaned_data, 'PresentCity')


    # Get user inputs
    age = st.number_input("Age", min_value=7, max_value=100)
    caste = st.selectbox("Caste", unique_castes)
    profession = st.selectbox("Profession", unique_professions)
    present_district = st.selectbox("Crime District", unique_districts)
    present_city = st.selectbox("Criminal Present City", unique_cities)

    # Perform Encoding
    f = open("../models/Recidivism_model/frequency_encoding.json")
    frequency = json.load(f)
    caste = frequency["Caste"][caste]
    profession = frequency["Profession"][profession]
    present_district = frequency["District_Name"][present_district]
    present_city = frequency["PresentCity"][present_city]


    # Create a new data point
    new_data = pd.DataFrame({
        'District_Name': [present_district],
        'age': [age],
        'Caste': [caste],
        'Profession': [profession],
        'PresentCity': [present_city],
    })

    # Perform Standardisation
    new_data_scaled = scaler.transform(new_data)

    new_df = pd.DataFrame(new_data_scaled, columns = new_data.columns, index = new_data.index)

    new_dataframe = h2o.H2OFrame(new_df)


    # Make a prediction
    if st.button("Predict"):
        
        # Make predictions
        predictions = model.predict(new_dataframe)

        # Convert H2OFrame to pandas DataFrame
        predictions_df = predictions.as_data_frame()

        # Extract the prediction
        pred = predictions_df.loc[0, "predict"]
        # Use the prediction
        if pred == 0:
            st.success("🔵 The person is not likely to repeat the crime.")
        else:
            st.warning("🔴 The person is likely to repeat the crime.")



def predictive_modeling_crime_type():
    st.subheader("Crime Type Prediction App")

    h2o.init()

    # Load the model
    model = load_model_crime_type()

    cleaned_data_crime_type = load_data_crime_type()
    # Get unique values for categorical features
    unique_district = get_unique_values_crime_type(cleaned_data_crime_type, 'District_Name')


    # Get user inputs
    district_name = st.selectbox("Enter District Name:", unique_district)
    offence_from_day = st.number_input("Offence From Day:", min_value=1, max_value=31)
    offence_from_month = st.number_input("Offence From Month:", min_value=1, max_value=12)
    offence_from_year = st.number_input("Offence From Year:", min_value=1927, max_value=2024)
    offence_to_day = st.number_input("Offence To Day:", min_value=1, max_value=31)
    offence_to_month = st.number_input("Offence To Month:", min_value=1, max_value=12)
    offence_to_year = st.number_input("Offence To Year:", min_value=1990, max_value=2024)




    # Create a new data point
    new_data_crime_type = pd.DataFrame({
        'District_Name': [district_name],
        'Offence_From_Year': [offence_from_year],
        'Offence_From_Month': [offence_from_month],
        'Offence_From_Day': [offence_from_day],
        'Offence_To_Year': [offence_to_year],
        'Offence_To_Month': [offence_to_month],
        'Offence_To_Day': [offence_to_day]
    })

    
    new_dataframe = h2o.H2OFrame(new_data_crime_type)

    # Make a prediction
    if st.button("Predict"):
        prediction = model.predict(new_dataframe)
        prediction = prediction.as_data_frame()['predict'][0]
        st.success(f"Predicted crime to be happen most is: {prediction}")

def generate_legend_html(category_to_color):
    legend_html = '<b>Crime Groups:</b><ul>'
    for category, color in category_to_color.items():
        legend_html += f'<li><span style="color:{color};">&#9632;</span> {category}</li>'
    legend_html += '</ul>'
    return legend_html




