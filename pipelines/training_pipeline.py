from Crime_Pattern_Analysis.ingest_data import *
from Crime_Pattern_Analysis.clean_data import *
from Criminal_Profiling.ingest_data import *
from Criminal_Profiling.clean_data import *
from Predictive_Modeling.ingest_data import *
from Predictive_Modeling.clean_data import *
from Predictive_Modeling.train_model import *

def crime_pattern_analysis():
    raw_data = ingest_crime_pattern_analysis()
    cleaned_data = clean_data_crime_pattern_analysis()
    update_crime_lat_long(cleaned_data)



def Criminal_profiling():
    raw_data = ingest_criminal_profiling()
    clean_Criminal_Profiling(raw_data)


def predictive_modeling():
    raw_data = ingest_recidivism_data()
    train, test = clean_recividism_model(raw_data) 
    best_model, test = train_recidivism_model(train, test)
    save_recidivism_explainability_plots(best_model, test)
    raw_data = ingest_hotspot_data()
    clean_hotspot_data(raw_data)




