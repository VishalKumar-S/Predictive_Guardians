import pandas as pd

def clean_Criminal_Profiling(Criminal_Profiling):

    features = ['Occupation', 'PresentCity', 'ActSection', 'Crime_Group1', 'Crime_Head2',  'Rowdy_Classification_Details', 'Activities_Description', 'PrevCase_Details', 'Caste' ]
    Criminal_Profiling[features] = Criminal_Profiling[features].fillna('unknown')

    Criminal_Profiling = Criminal_Profiling[['Occupation', 
       'Crime_Group1', 'Crime_Head2','age',
       'Caste', 'Sex']]


    Criminal_Profiling.to_csv("../datasets/Criminal Profiling/Criminal_Profiling_cleaned.csv")




