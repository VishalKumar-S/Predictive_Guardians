import pandas as pd

def clean_Criminal_Profiling():
    clean_data = pd.read_csv("datasets\Criminal Profiling\Criminal_Profiling_raw.csv")

    features = ['Occupation', 'PresentCity', 'ActSection', 'Crime_Group1', 'Crime_Head2',  'Rowdy_Classification_Details', 'Activities_Description', 'PrevCase_Details', 'Caste' ]
    clean_data[features] = clean_data[features].fillna('unknown')

    clean_data.to_csv("datasets\Criminal Profiling\Criminal_Profiling_cleaned.csv")




clean_Criminal_Profiling()