import math
import pandas as pd
import re
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

def ingest_crime_pattern_analysis():
    fir_details = pd.read_csv("datasets/FIR_Details_Data.csv")
    logging.info("Ingested the raw datasets for Crime Pattern Analysis")

    #Select relevant columns from FIR dataset
    fir_relevant = fir_details[['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month',
    'FIR_Reg_DateTime', 'CrimeGroup_Name', 'CrimeHead_Name', 'Latitude', 'Longitude', 'Distance from PS', 'VICTIM COUNT', 'Accused Count']]


    raw_data = pd.DataFrame(fir_relevant)
    raw_data.to_csv('datasets/Crime Pattern Analysis/Crime_Pattern_Analysis_Raw.csv', index=False)

    logging.info(" Raw dataset sucessfully created for the Crime Pattern Analysis Component")


ingest_crime_pattern_analysis()