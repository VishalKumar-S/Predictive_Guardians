import pandas as pd


def ingest_resource_data():
    df = pd.read_csv("../datasets/FIR_Details_Data.csv")

    df.drop(columns= df.columns[~df.columns.isin(['District_Name', 'UnitName', 'FIRNo', 'CrimeGroup_Name',
            'Beat_Name', 'Village_Area_Name', 'Accused Count',
        'Arrested Count\tNo.',
        'Accused_ChargeSheeted Count',
        ])],inplace = True)

    df.drop_duplicates(inplace =  True)

    return df