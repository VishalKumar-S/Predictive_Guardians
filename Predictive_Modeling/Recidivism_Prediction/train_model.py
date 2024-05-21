import h2o
from h2o.automl import H2OAutoML
import pandas as pd
from sklearn.model_selection import train_test_split



def train_recidivism_model(cleaned_data):

    h2o.init()
    dataset = h2o.H2OFrame(cleaned_data)
    train, test = dataset.split_frame(ratios=[0.7])

    # Convert the 'Recidivism' column to categorical
    train['Recidivism'] = train['Recidivism'].asfactor()
    test['Recidivism'] = test['Recidivism'].asfactor()


    # Specify the target variable and input features
    y = "Recidivism"
    x = train.columns
    x.remove(y)

    # Run the AutoML process
    aml = H2OAutoML(seed=42, max_runtime_secs = 30)
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




