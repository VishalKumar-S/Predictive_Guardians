import math
import pandas as pd
import re
import logging
import sys
from sklearn.model_selection import train_test_split


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])



def clean_data_crime_pattern_analysis(clean_df):

    #Drop Duplicates
    clean_df.drop_duplicates(inplace = True)
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
    logging.info("District names are renamed, to match with the geojson district map names of Karnataka to use it as a base map, for geo-spatial analysis")

    # Impute unknown values in 'Distance from PS" column
    columns_to_impute_unknown = ['Distance from PS']

    clean_df[columns_to_impute_unknown] = clean_df[columns_to_impute_unknown].fillna('Unknown')

    logging.info(" Missing observations are imputed")

    crime_pattern_analysis = clean_df.copy()

    #Get Karnataka Police Stations and their unit's lat-long details
    PS_lat_long = pd.read_csv('../datasets/Polce_Stations_Lat_Long.csv')

    # merge both datasets
    crime_data = pd.merge(crime_pattern_analysis,PS_lat_long, on = "UnitName", suffixes=('_first', '_second'))

    # Impute latitude and longitude values
    crime_data['Latitude_first'] = crime_data['Latitude_second']
    crime_data['Longitude_first'] = crime_data['Longitude_second']


    # Drop unnecessary column
    crime_data = crime_data.drop(['Latitude_second', 'Longitude_second'], axis=1)
  
    # Rename the features
    crime_data = crime_data.rename(columns={"Latitude_first": "Latitude", "Longitude_first": "Longitude"})

    logging.info(" Imputed missing crime's latitude and longitude with temporary values as Police station's co-ordinates")

    # Extract date value alone from FIR_Reg_DateTime
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
  # This method is used to extract the distance, it's unit measured and convert all the units to standarised unit of KM and the direction of the crime from the Police Station in the string

  # Distance units pattern reg-x (m-metres,f-feet, k- refers to KM observations)

  distance_pattern = r'\d+'

  #Filter only meters, exlcudes KM's and feet  and convert it to KM
  if not re.search(r'k', string, re.IGNORECASE) and not re.search(r'feet', string, re.IGNORECASE) and re.search(r'm', string, re.IGNORECASE):
    match = re.search(distance_pattern, string)
    if match:
      distance = int(match.group())/1000
    else:
      distance = 0

  #Filter only feet, exlcudes KM's and meters and convert it to KM
  elif not re.search(r'k', string, re.IGNORECASE) and re.search(r'feet', string, re.IGNORECASE):
    match = re.search(distance_pattern, string)
    if match:
      distance = 0
    else:
      distance = 0

  # Distance is already in KM only, no need to convert type.
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

  #Handle any other human- errored wrong distance metric names    
  else:
    distance = 0

  # Extract the direction from the string
  direction_pattern = r'\b(?:north|south|east|west)\b'

  # re.IGNORECASE is used for case-insensitive matching
  match = re.search(direction_pattern, string, re.IGNORECASE)
  if match:
    matched_string = match.group()  
    # Extract the matched string using match.group()
    direction = matched_string
  else:
      direction = 'None'
  return direction, distance



def calculate_crime_coordinates(lat, lon, direction, distance):
    ##Here, we convert the lat and long from degrees to radians, to update the values, We can't update the lat and long if it's in degrees itself, to add the distance between the crime location and police station to the police station's latitude and longitude, to find the actual crime'ss location, we need to  convert the distances to angular distance, by dividing the actual distance by earth's radius, since arc length i.e distance travelled between 2 points (police station and crime location) in teh surface of a sphere (earth), = Teta*radius, i.e Angular distance teta in radians =  distance/radius.


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
        # Invalid direction, return original coordinates as we cannot identify the crime location
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




