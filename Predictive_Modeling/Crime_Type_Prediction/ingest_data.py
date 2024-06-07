import pandas as pd

def ingest_crime_type_data():
    df = pd.read_csv("../datasets/FIR_Details_Data.csv")

    return df