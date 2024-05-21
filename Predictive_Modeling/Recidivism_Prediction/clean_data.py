import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
import random

def clean_recividism_model(acused):
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

    
    balanced_data.to_csv("../Component_datasets/Recidivism_cleaned_data.csv")

    return balanced_data


