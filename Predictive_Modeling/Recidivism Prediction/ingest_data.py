import pandas as pd



def ingest_recidivism_data():
   acused = pd.read_csv("../../datasets/AccusedData.csv")

   acused = acused[(acused['age'] <= 100) & (acused['age'] >= 7)]

   clean_acused =  acused.drop(['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'AccusedName',
      'Person_Name',  'PresentAddress',
      'PermanentAddress', 'PermanentCity',
      'PermanentState','Nationality_Name', 'DOB',  'Arr_ID', 'crime_no'], axis =1)

   
   # Assuming 'clean_acused' is your DataFrame after dropping rows with missing values
   clean_acused = clean_acused.dropna(subset=['age', 'Caste', 'Profession', 'Sex', 'PresentCity', 'PresentState', 'Person_No' ])
   clean_acused.reset_index(drop=True, inplace=True)  # Corrected the reset_index operation

   clean_acused = clean_acused.drop_duplicates()


   clean_acused['Recidivism'] = clean_acused['Person_No'].map(lambda x: 1 if acused_count[x] > 1 else 0)

   clean_acused= clean_acused.drop('Person_No', axis =1)

   clean_acused = clean_acused.drop_duplicates()
   clean_acused.reset_index(drop = True,inplace = True )

   clean_acused.to_csv("datasets/Predictive Modeling/Recidivism_cleaned_data.csv")

   return clean_acused



