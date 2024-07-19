import h2o
from h2o.automl import H2OAutoML
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler





def train_recidivism_model(cleaned_data):

    #Perform Standardisation
    X = cleaned_data.drop('Recidivism', axis=1)
    y = cleaned_data['Recidivism']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)


    h2o.init()
    train = h2o.H2OFrame(X_train_scaled_df.join(y_train))
    test = h2o.H2OFrame(X_test_scaled_df.join(y_test))

    # Convert the 'Recidivism' column to categorical
    train['Recidivism'] = train['Recidivism'].asfactor()
    test['Recidivism'] = test['Recidivism'].asfactor()


    # Specify the target variable and input features
    y = "Recidivism"
    x = train.columns
    x.remove(y)

    # Run the AutoML process
    aml = H2OAutoML(seed=42, max_runtime_secs = 900)
    aml.train(x=x, y=y, training_frame=train)

    # Get the leaderboard of models
    lb = aml.leaderboard
    lb.head(rows=lb.nrows)

    # Select the best model from the leaderboard
    best_model = aml.leader

    model_type = best_model.model_id
    print(model_type)

    best_model.download_mojo("../models/Recidivism_model", get_genmodel_jar=True)

    # Evaluate the best model on the test set
    performance = best_model.model_performance(test)
    print(performance)

    # Make predictions on the test set
    predictions = best_model.predict(test)






# def save_recidivism_explainability_plots(model, data):
#     obj = model.explain(data, render=False)
#     for key in obj.keys():
#         print(f"saving {key} plots")
#         if not obj.get(key).get("plots"):
#             continue
#         plots = obj.get(key).get("plots").keys()

#         os.makedirs(f"./images/{key}", exist_ok=True)
#         for plot in plots:
#             fig = obj.get(key).get("plots").get(plot).figure()
#             fig.savefig(f"./images/{key}/{plot}.png")




