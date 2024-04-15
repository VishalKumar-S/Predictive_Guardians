import pandas as pd


def ingest_resource_data():
    df = pd.read_csv("../datasets/FIR_Details_Data.csv")
    resource_relevant = df[['District_Name', 'UnitName', 'Village_Area_Name',  'CrimeGroup_Name', 'Beat_Name']]

    resource_relevant.drop_duplicates(inplace =  True)

    return resource_relevant