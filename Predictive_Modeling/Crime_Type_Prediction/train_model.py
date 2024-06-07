import h2o
from h2o.automl import H2OAutoML



def train_crime_type_model(cleaned_data):
    # Initialize H2O cluster
    h2o.init()

    # Load data as H2OFrame
    h20_frame = h2o.H2OFrame(cleaned_data)
    # Specify the response and predictor columns
    response = "Crime Category"
    predictors = h20_frame.columns.remove(response)

    # Split the data into train and test
    train, test = h20_frame.split_frame(ratios=[.8])

    # Run AutoML
    aml = H2OAutoML(seed=42, max_runtime_secs= 900)
    aml.train(x=predictors, y=response, training_frame=train)
    # Get the leaderboard of models
    lb = aml.leaderboard
    lb.head(rows=lb.nrows)

    # Select the best model from the leaderboard
    best_model = aml.leader

    model_type = best_model.model_id
    print(model_type)

    best_model.download_mojo("../models/Crime_Type_Prediction", get_genmodel_jar=True)

    # Evaluate the best model on the test set
    performance = best_model.model_performance(test)
    print(performance)

    # Make predictions on the test set
    predictions = best_model.predict(test)

