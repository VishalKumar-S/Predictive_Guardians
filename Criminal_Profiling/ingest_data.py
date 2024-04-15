import pandas as pd

def ingest_criminal_profiling():
    MOB = pd.read_csv("../datasets/MOBsData.csv")
    rowdy = pd.read_csv("../datasets/RowdySheeterDetails.csv")
    accused = pd.read_csv("../datasets/AccusedData.csv")

    accused = accused[(accused['age'] <= 100) & (accused['age'] >= 7) ]

    accused =  accused.rename(columns = {'UnitName': 'Unit_Name'})
    accused =  accused.rename(columns = {'AccusedName': 'Name'})

    mob_relevant = MOB[['District_Name', 'Unit_Name', 'Name',
       'Occupation', 'ActSection', 'Crime_Group1',
       'Crime_Head2',
       ]]

    rowdy_relevant = rowdy[['District_Name', 'Unit_Name', 'Name',
      'Rowdy_Classification_Details',
       'Activities_Description',  'PrevCase_Details']]

    accused_relevant = accused[['District_Name', 'Unit_Name', 'Year', 'Month', 'Name',
        'age', 'Caste',  'Sex', 'PresentAddress', 'PresentCity']]

    merge = pd.merge(mob_relevant, rowdy_relevant,  on = ['District_Name', 'Unit_Name', 'Name',], how = 'inner' )
    merge = pd.merge(merge, accused_relevant,  on = ['District_Name', 'Unit_Name', 'Name', ], how = 'inner' )

    Criminal_Profiling = pd.DataFrame(merge)

    Criminal_Profiling = Criminal_Profiling.drop_duplicates()

    return Criminal_Profiling

