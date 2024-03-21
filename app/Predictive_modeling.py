import sreamlit as st
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



@st.cache_data
def load_data()
    return pd.read_csv("datasets/Predictive Modeling/Recidivism_cleaned_data.csv")

# Load the model
@st.cache_resource
def load_model():
    saved_model = h2o.import_mojo("models/Recidivism_model/XGBoost_1_AutoML_1_20240321_35815.zip")
    return saved_model

def get_unique_values(data, feature):
    return data[feature].unique().tolist()

# Load the saved TargetEncoder
@st.cache_resource
def load_target_encoder():
    with open('models/Recidivism_model/target_encoder.pkl', 'rb') as file:
        target_encoder = pickle.load(file)
    return target_encoder

# Function to preprocess new data
def preprocess_data(data):
    # Load the saved TargetEncoder
    target_encoder = load_target_encoder()

    # Encoding categorical features using the saved TargetEncoder
    categorical_features = ['Caste', 'Profession', 'PresentCity', 'PresentState']
    X[categorical_features] = target_encoder.transform(X[categorical_features])

    return X

def predictive_modeling():
    st.subheader("Recidivism Prediction App")

    # Load the model
    model = load_model()

    cleaned_data = load_data()
    # Get unique values for categorical features
    unique_castes = get_unique_values(cleaned_data, 'Caste')
    unique_professions = get_unique_values(cleaned_data, 'Profession')
    unique_cities = get_unique_values(cleaned_data, 'PresentCity')
    unique_states = get_unique_values(cleaned_data, 'PresentState')

    # Get user inputs
    age = st.number_input("Age", min_value=7, max_value=100)
    caste = st.selectbox("Caste", unique_castes)
    profession = st.selectbox("Profession", unique_professions)
    sex = st.selectbox("Sex", ["Male", "Female"])
    if sex == "Male":
        Male = 1
        Female = 0
    if sex == "Female":
        Male = 0
        Female = 1

    present_city = st.selectbox("Present City", unique_cities)
    present_state = st.selectbox("Present State", unique_states)

    # Create a new data point
    new_data = pd.DataFrame({
        'age': [age],
        'Caste': [caste],
        'Profession': [profession],
        'PresentCity': [present_city],
        'PresentState': [present_state]
        'FEMALE': [Female],
        'MALE': [Male]
    })

    # Preprocess the new data
    new_data_processed = preprocess_data(new_data)

    new_dataframe = h2o.H2OFrame(new_data_processed)

    # Make a prediction
    if st.button("Predict"):
        prediction = model.predict(new_data_processed)
        if prediction[0] == 0:
            st.success("The person is not likely to repeat the crime.")
        else:
            st.warning("The person is likely to repeat the crime.")

