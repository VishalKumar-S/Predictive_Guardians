import pandas as pd



def ingest_recidivism_data():
   acused = pd.read_csv("../datasets/AccusedData.csv")

   acused.dropna(subset = ['age', 'Caste', 'Profession', 'Sex',
       'PresentCity', 'PresentState', 'Person_No'], inplace = True)
      
   acused.drop_duplicates(inplace = True)

   # Count the number of occurrences for each Person_No and Arr_ID combination
   acused['Recidivism'] = acused.groupby(['Person_No', 'Arr_ID'])['Person_No'].transform('size') > 1

   # Convert boolean to integer (1 for True, 0 for False)
   acused['Recidivism'] = acused['Recidivism'].astype(int)

   acused.drop(columns = [ 'UnitName', 'FIRNo', 'Year', 'Month', 'AccusedName',
       'Person_Name','PresentAddress','PermanentAddress', 'PermanentCity',
       'PermanentState', 'Nationality_Name', 'DOB', 'Person_No', 'Arr_ID',
       'crime_no','PresentState','Sex'], inplace = True)
      
   acused.drop_duplicates(inplace = True)

   acused = acused[(acused["age"]>7) & (acused["age"]<=100)]

   return acused



