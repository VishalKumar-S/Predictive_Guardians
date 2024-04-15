import pandas as pd


def ingest_hotspot_data():
    return pd.read_csv("../../datasets/Criminal Profiling/Criminal_Profiling.csv")