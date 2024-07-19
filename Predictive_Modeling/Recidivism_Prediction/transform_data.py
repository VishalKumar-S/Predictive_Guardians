import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def frequency_encoding(cleaned_data):
    # Frequency/ Count Encoding
    categorical_columns = ['District_Name', 'Caste', 'Profession', 'PresentCity']

    value_count_dict = {}
    for col in categorical_columns:
        value = cleaned_data[col].value_counts()
        value_count_dict[col] = value.to_dict()
        cleaned_data[col] = cleaned_data[col].map(value_count_dict[col])


    output_dir = os.path.abspath('../models/Recidivism_model')
    encoding_file_path = os.path.join(output_dir, 'frequency_encoding.json')

    

    # Automatically create the directory if it does not exist
    if not os.path.exists(encoding_file_path):
        os.makedirs(encoding_file_path)


    # Example for saving frequency encoding dictionary
    frequency_encoding = {}  # Replace with your actual encoding dictionary
    with open(encoding_file_path, 'w') as f:
        json.dump(value_count_dict, f)
        print("saved json file")
    
    return cleaned_data
    




def standardise_data(encoded_data):
    #Perform Standardisation
    X = encoded_data.drop('Recidivism', axis=1)
    y = encoded_data['Recidivism']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    output_dir = os.path.abspath('../models/Recidivism_model')
    scaler_file_path = os.path.join(output_dir, 'scaler.pkl')

    with open(scaler_file_path,'w') as f:
        joblib.dump(scaler, scaler_file_path)
        print("dumped scaler successfully")

    X_test_scaled = scaler.transform(X_test)

    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

    return X_train_scaled_df, X_test_scaled_df, y_train, y_test 





def transform_cleaned_recidivism_data(cleaned_data):
    encoded_data = frequency_encoding(cleaned_data)
    X_train, X_test, y_train, y_test = standardise_data(encoded_data)
    return X_train, X_test, y_train, y_test


    
    