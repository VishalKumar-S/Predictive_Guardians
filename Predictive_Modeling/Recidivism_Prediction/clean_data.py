import pandas as pd
from category_encoders import TargetEncoder
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pickle

def clean_recividism_model(clean_acused):
    # Separate features and target
    X = clean_acused.drop('Recidivism', axis=1)
    y = clean_acused['Recidivism']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Encoding categorical features using TargetEncoder for training data
    categorical_features = ['Caste', 'Profession', 'PresentCity', 'PresentState']
    categorical_transformer = TargetEncoder(cols=categorical_features)
    X_train[categorical_features] = categorical_transformer.fit_transform(X_train[categorical_features], y_train)

    # Encoding categorical features using TargetEncoder for testing data
    X_test[categorical_features] = categorical_transformer.transform(X_test[categorical_features])

    # Encoding 'Sex' feature using OneHotEncoder for training data
    sex_encoder = OneHotEncoder(handle_unknown='ignore', drop='first')
    X_train = pd.concat([X_train.drop('Sex', axis=1), pd.get_dummies(X_train['Sex'], drop_first=True)], axis=1)

    # Save the fitted TargetEncoder
    with open('models/Recidivism_model/target_encoder.pkl', 'wb') as file:
        pickle.dump(categorical_transformer, file)

    # Encoding 'Sex' feature using OneHotEncoder for testing data
    X_test = pd.concat([X_test.drop('Sex', axis=1), pd.get_dummies(X_test['Sex'], drop_first=True)], axis=1)

    # Oversampling using SMOTE only on the training data
    smote = SMOTE(random_state=42)
    X_resampled_train, y_resampled_train = smote.fit_resample(X_train, y_train)

    train = pd.concat([pd.DataFrame(X_resampled_train), pd.DataFrame(y_resampled_train, columns=['Recidivism'])], axis=1)
    test = pd.concat([pd.DataFrame(X_test), pd.DataFrame(y_test, columns=['Recidivism'])], axis=1)

    
    return train, test



