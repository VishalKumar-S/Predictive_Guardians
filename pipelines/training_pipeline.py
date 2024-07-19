import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)


from Crime_Pattern_Analysis.ingest_data import *
from Crime_Pattern_Analysis.clean_data import *
from Criminal_Profiling.ingest_data import *
from Criminal_Profiling.clean_data import *
from Predictive_Modeling.Crime_Hotspot_Prediction.ingest_data import *
from Predictive_Modeling.Crime_Hotspot_Prediction.clean_data import *
from Predictive_Modeling.Recidivism_Prediction.ingest_data import *
from Predictive_Modeling.Recidivism_Prediction.clean_data import *
from Predictive_Modeling.Recidivism_Prediction.train_model import *
from Predictive_Modeling.Recidivism_Prediction.transform_data import *
from Resource_Allocation.ingest_data import *
from Resource_Allocation.clean_data import *
from Predictive_Modeling.Crime_Type_Prediction.ingest_data import *
from Predictive_Modeling.Crime_Type_Prediction.clean_data import *
from Predictive_Modeling.Crime_Type_Prediction.train_model import *





def crime_pattern_analysis():
    raw_data = ingest_crime_pattern_analysis()
    cleaned_data = clean_data_crime_pattern_analysis()
    cleaned_data = update_crime_lat_long(cleaned_data)


def Criminal_profiling():
    raw_data = ingest_criminal_profiling()
    clean_Criminal_Profiling(raw_data)


def predictive_modeling():
    raw_data = ingest_recidivism_data()
    cleaned_data = clean_recividism_model(raw_data)
    X_train, X_test, y_train, y_test = transform_cleaned_recidivism_data(cleaned_data) 
    train_recidivism_model(X_train, X_test, y_train, y_test)
    raw_data =  ingest_crime_type_data()
    cleaned_data =  clean_Crime_type_data(raw_data)
    train_crime_type_model(cleaned_data)
    raw_data = ingest_hotspot_data()
    clean_hotspot_data(raw_data)

def resource_allocation():
    raw_data = ingest_resource_data()
    cleaned_data = clean_resource_data(raw_data)
    feature_engineering_resources(cleaned_data)





crime_pattern_analysis()
Criminal_profiling()
predictive_modeling()
resource_allocation()





