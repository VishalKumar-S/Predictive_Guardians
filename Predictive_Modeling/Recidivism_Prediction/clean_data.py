import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
import random

def clean_recividism_model(acused):
    #SMOTE
    # Split the acused into majority and minority classes
    majority_class = acused[acused['Recidivism'] == 1]

    minority_class = acused[acused['Recidivism'] == 0]

    desired_ratio = len(minority_class) / len(majority_class)



    # Randomly undersample the majority class
    undersampled_majority = random.sample(list(majority_class.index), int(len(majority_class) * desired_ratio))

    undersampled_majority_class = majority_class.loc[undersampled_majority]

    undersampled_data = pd.concat([undersampled_majority_class, minority_class])

    # Combine majority and minority classes
    X = acused.drop('Recidivism', axis=1)
    y = acused['Recidivism']

    # Oversample the minority class
    oversample = RandomOverSampler(sampling_strategy='minority')
    X_oversampled, y_oversampled = oversample.fit_resample(X, y)
    oversampled_data = pd.concat([X_oversampled, y_oversampled], axis=1)

    # Undersample the majority class
    undersample = RandomUnderSampler(sampling_strategy='majority')
    X_undersampled, y_undersampled = undersample.fit_resample(X, y)
    undersampled_data = pd.concat([X_undersampled, y_undersampled], axis=1)

    # Combine the oversampled and undersampled data
    balanced_data = pd.concat([oversampled_data, undersampled_data])


    # Reduce High Cardinality in Categorical Variables

    categorical_columns = balanced_data.select_dtypes(include=['object']).columns  # Get all categorical columns
    threshold_percentage=1
    
    for column in categorical_columns:
        value_counts = balanced_data[column].value_counts(normalize=True) * 100
        # Replace categories below the threshold with 'Other'
        balanced_data[column] = balanced_data[column].apply(lambda x: x if value_counts.get(x, 0) >= threshold_percentage else 'Other')

    
    # Frequency/ Count Encoding
    categorical_columns = ['District_Name', 'Caste', 'Profession', 'Sex', 'PresentCity', 'PresentState']

    value_count_dict = {}
    for col in categorical_columns:
        value = balanced_data[col].value_counts()
        value_count_dict[col] = value
        balanced_data[col] = balanced_data[col].map(value)

    with open('models/Recidivism_model/frequency_encoding.json', 'w') as f:
        json.dump(value_count_dict, f)

    
    balanced_data.to_csv("../Component_datasets/Recidivism_cleaned_data.csv")

    return balanced_data


