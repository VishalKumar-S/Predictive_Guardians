import math
import pandas as pd
import re
import logging
import sys
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])



def clean_data_crime_pattern_analysis():
    clean_df= pd.read_csv("../datasets/Crime Pattern Analysis/Crime_Pattern_Analysis_Raw.csv")

    #Drop Duplicates
    clean_df = clean_df.drop_duplicates()
    logging.info(" Duplicate observations are removed")

    #Rename features
    clean_df['District_Name'] = clean_df['District_Name'].replace({
        'Bengaluru City': 'Bengaluru Urban',
        'Belagavi Dist': 'Belagavi',
        'Bengaluru Dist': 'Bengaluru Rural',
        'Bagalkot': 'Bagalkote',
        'Chamarajanagar': 'Chamarajanagara',
        'Belagavi City': 'Belagavi',
        'Chickballapura': 'Chikkaballapura',
        'Mysuru City': 'Mysuru',
        'Vijayanagara': 'Vijayapura',
        'Kalaburagi City': 'Kalaburagi',         
        'Hubballi Dharwad City':'Dharwad' 
    }) 
    logging.info("District names are renamed, to match with the geojson district map of Karnataka to use it as a base map, for further geo-spatial analysis")

    # Impute unknown
    columns_to_impute_unknown = ['Distance from PS']

    clean_df[columns_to_impute_unknown] = clean_df[columns_to_impute_unknown].fillna('Unknown')

    logging.info(" Missing observations are imputed")

    #Impute Latitude and Longitude values
    # Load  datasets
    crime_pattern_analysis = clean_df.copy()
    PS_lat_long = pd.read_csv('../datasets/Crime Pattern Analysis/Polce_Stations_Lat_Long.csv')

    # merge both datasets
    crime_data = pd.merge(crime_pattern_analysis,PS_lat_long, on = "UnitName", suffixes=('_first', '_second'))

    # Impute latitude and longitude values
    crime_data['Latitude_first'] = crime_data['Latitude_second']
    crime_data['Longitude_first'] = crime_data['Longitude_second']

    # Drop unnecessary columns
    crime_data = crime_data.drop(['Latitude_second', 'Longitude_second'], axis=1)
  
    # Rename the features
    crime_data = crime_data.rename(columns={"Latitude_first": "Latitude", "Longitude_first": "Longitude"})

    logging.info(" Imputed missing crime's latitude and longitude with temporary values as Police station's co-ordinates")

    # Preprocess FIR_Reg_DateTime to extract date features only
    crime_data['FIR_Reg_Date'] = crime_data['FIR_Reg_DateTime'].str.split(' ').str[0]

    # Convert FIR_Reg_Date to datetime format
    crime_data['FIR_Reg_Date'] = pd.to_datetime(crime_data['FIR_Reg_Date'])

    # Extract year, month, and day
    crime_data['Year'] = crime_data['FIR_Reg_Date'].dt.year
    crime_data['Month'] = crime_data['FIR_Reg_Date'].dt.month
    crime_data['Day'] = crime_data['FIR_Reg_Date'].dt.day

    remove_reductant_features = ["FIR_Reg_Date","FIR_Reg_DateTime"]
    crime_data = crime_data.drop(remove_reductant_features, axis = 1)

    logging.info(" Proper date features are extracted from the 'FIR_Reg_Date' feature ")

    return crime_data



def extract_direction_distance(string):

  # Distance units pattern reg-x (m-metres,f-feet, k- refers to KM observations)
  distance_pattern = r'\d+'
  if not re.search(r'k', string, re.IGNORECASE) and not re.search(r'feet', string, re.IGNORECASE) and re.search(r'm', string, re.IGNORECASE):
    match = re.search(distance_pattern, string)
    if match:
      distance = int(match.group())/1000
    else:
      distance = 0
  elif not re.search(r'k', string, re.IGNORECASE) and re.search(r'feet', string, re.IGNORECASE):
    match = re.search(distance_pattern, string)
    if match:
      distance = 0
    else:
      distance = 0
  elif re.search(r'k', string, re.IGNORECASE):
    match = re.search(distance_pattern, string)
    if match:
      distance = int(match.group())
      # Handle outlier/ wrongly written KM distance values
      distance_count = len(str(distance))
      if distance_count > 2:
        distance = 0
    else:
      distance = 0
  else:
    distance = 0

  direction_pattern = r'\b(?:north|south|east|west)\b'
  match = re.search(direction_pattern, string, re.IGNORECASE)  # Using re.IGNORECASE to perform case-insensitive matching
  if match:
    matched_string = match.group()  # Extract the matched string using match.group()
    direction = matched_string
  else:
      direction = 'None'
  return direction, distance



def calculate_crime_coordinates(lat, lon, direction, distance):
    # Earth radius in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # Convert distance from kilometers to radians
    angular_distance = distance / earth_radius

    # Calculate new latitude and longitude based on direction
    if direction == 'NORTH':
        new_lat = math.degrees(lat_rad + angular_distance)
        new_lon = lon
    elif direction == 'SOUTH':
        new_lat = math.degrees(lat_rad - angular_distance)
        new_lon = lon
    elif direction == 'EAST':
        new_lat = lat
        new_lon = math.degrees(lon_rad + angular_distance)
    elif direction == 'WEST':
        new_lat = lat
        new_lon = math.degrees(lon_rad - angular_distance)
    else:
        # Invalid direction, return original coordinates
        new_lat = lat
        new_lon = lon

    return new_lat, new_lon




def update_crime_lat_long(new_data):
    logging.info("Started to impute accurate crime's co-ordinates by calculating the crime's direction, distance and it's unit(Km/m/feet) away from the police station co-ordinates details from the dataset ...")
    for index, row in new_data.iterrows():
        direction, distance = extract_direction_distance(row["Distance from PS"])
        if direction and distance is not None:
            new_lat, new_lon = calculate_crime_coordinates(row["Latitude"], row["Longitude"], direction, distance)
            new_data.at[index, "Latitude"] = new_lat
            new_data.at[index, "Longitude"] = new_lon
        else:
            print(f"Error: Unable to extract direction and distance for row {index}.")

    # Remove redundant feature
    new_data = new_data.drop("Distance from PS", axis=1)

    # Remove outlier co-ordinates
    
    new_data = new_data[~((new_data["Latitude"] > 19) |
                            (new_data["Longitude"] > 78) |
                            (new_data["Latitude"] < 11) |
                            (new_data["Longitude"] < 74))]

    # Save the new dataset to a new CSV file
    new_data.to_csv("../Component_datasets/Crime_Pattern_Analysis_Cleaned.csv", index=False)

    logging.info("Dataset is processed and ready with accurate crime co-ordinates now")

    return new_data




