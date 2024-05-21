import pandas as pd
import re

def clean_resource_data(clean_data):
    #Rename features
    clean_data['District_Name'] = clean_data['District_Name'].replace({
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
        'Hubballi Dharwad City':'Dharwad',
        'Shivamogga': "Shimoga",
        "Mysuru Dist": "Mysuru",
        "Mangaluru City": "Dakshina Kannada",
        "Chikkamagaluru": "Chikmagalur",
        "K.G.F": "Kolar",
        "Coastal Security df": "Udupi",
        "ISD Bengaluru": "Bengaluru Urban",
        "CID":"Bengaluru Urban",
    })



    category_mapping = {
        'THEFT': 'Property Crimes',
        'BURGLARY - NIGHT': 'Property Crimes',
        'BURGLARY - DAY': 'Property Crimes',
        'ROBBERY': 'Property Crimes',
        'DACOITY': 'Property Crimes',
        'CRIMINAL BREACH OF TRUST': 'Property Crimes',
        'CHEATING': 'Property Crimes',
        'FORGERY': 'Property Crimes',
        'COUNTERFEITING': 'Property Crimes',
        'CRIMINAL MISAPPROPRIATION ': 'Property Crimes',
        'RECEIVING OF STOLEN PROPERTY': 'Property Crimes',
        'MOTOR VEHICLE ACCIDENTS NON-FATAL': 'Accidents and Public Safety',
        'MOTOR VEHICLE ACCIDENTS FATAL': 'Accidents and Public Safety',
        'DEATHS DUE TO RASHNESS/NEGLIGENCE': 'Accidents and Public Safety',
        'NEGLIGENT ACT': 'Accidents and Public Safety',
        'PUBLIC SAFETY': 'Accidents and Public Safety',
        'PUBLIC NUISANCE': 'Accidents and Public Safety',
        'MISSING PERSON': 'Missing Persons',
        ' CYBER CRIME': 'Cyber Crimes',
        'CASES OF HURT': 'Violent Crimes',
        'ATTEMPT TO MURDER': 'Violent Crimes',
        'MURDER': 'Violent Crimes',
        'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'Violent Crimes',
        'ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'Violent Crimes',
        'MOLESTATION': 'Violent Crimes',
        'KIDNAPPING AND ABDUCTION': 'Violent Crimes',
        'RIOTS': 'Violent Crimes',
        'CRUELTY BY HUSBAND': 'Violent Crimes',
        'CRIMES RELATED TO WOMEN': 'Violent Crimes',
        'POCSO': 'Violent Crimes',
        'CRIMINAL INTIMIDATION': 'Violent Crimes',
        'WRONGFUL RESTRAINT/CONFINEMENT': 'Violent Crimes',
        'INSULTING MODESTY OF WOMEN (EVE TEASING)': 'Violent Crimes',
        'ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN': 'Violent Crimes',
        'EXPOSURE AND ABANDONMENT OF CHILD': 'Violent Crimes',
        'DOWRY DEATHS': 'Violent Crimes',
        'OFFENCES RELATED TO MARRIAGE': 'Violent Crimes',
        'ASSAULT': 'Violent Crimes',
        'CRIMINAL TRESPASS': 'Violent Crimes',
        'MISCHIEF': 'Violent Crimes',
        'ARSON': 'Violent Crimes',
        'CRIMINAL CONSPIRACY': 'Violent Crimes',
        'AFFRAY': 'Violent Crimes',
        'CrPC': 'Legal and Regulatory Offenses',
        'KARNATAKA df ACT 1963': 'Legal and Regulatory Offenses',
        'Karnataka State Local Act': 'Legal and Regulatory Offenses',
        'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES': 'Legal and Regulatory Offenses',
        'COTPA, CIGARETTES AND OTHER TOBACCO PRODUCTS': 'Legal and Regulatory Offenses',
        'COPY RIGHT ACT 1957': 'Legal and Regulatory Offenses',
        'ARMS ACT  1959': 'Legal and Regulatory Offenses',
        ' PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984': 'Legal and Regulatory Offenses',
        ' REPRESENTATION OF PEOPLE ACT 1951 & 1988': 'Legal and Regulatory Offenses',
        'PASSPORT ACT': 'Legal and Regulatory Offenses',
        'EXPLOSIVES': 'Legal and Regulatory Offenses',
        'OFFENCES PROMOTING ENEMITY': 'Legal and Regulatory Offenses',
        'Concealment of birth by secret disposal of Child': 'Legal and Regulatory Offenses',
        'PORNOGRAPHY': 'Legal and Regulatory Offenses',
        'ADULTERATION': 'Legal and Regulatory Offenses',
        'POISONING-PROFESSIONAL': 'Legal and Regulatory Offenses',
        'SLAVERY': 'Legal and Regulatory Offenses',
        'OFFENCES BY PUBLIC SERVANTS (EXCEPT CORRUPTION) (Public servant is accused)': 'Legal and Regulatory Offenses',
        'BONDED LABOUR SYSTEM': 'Legal and Regulatory Offenses',
        'FOREST': 'Legal and Regulatory Offenses',
        'INDIAN ELECTRICITY ACT ': 'Legal and Regulatory Offenses',
        'INDIAN MOTOR VEHICLE': 'Legal and Regulatory Offenses',
        'UNNATURAL SEX ': 'Legal and Regulatory Offenses',
        'IMPERSONATION ': 'Legal and Regulatory Offenses',
        'PUBLIC JUSTICE': 'Legal and Regulatory Offenses',
        'OF ABETMENT': 'Legal and Regulatory Offenses',
        ' POST & TELEGRAPH,TELEGRAPH WIRES(UNLAWFUL POSSESSION)ACT 1950': 'Legal and Regulatory Offenses',
        'Human Trafficking': 'Legal and Regulatory Offenses',
        'ANTIQUES (CULTURAL PROPERTY)': 'Legal and Regulatory Offenses',
        'OFFICIAL SECURITY RELATED ACTS': 'Legal and Regulatory Offenses',
        'UNLAWFUL ACTIVITIES(Prevention)ACT 1967 ': 'Legal and Regulatory Offenses',
        'SEDITION': 'Legal and Regulatory Offenses',
        'DOCUMENTS & PROPERTY MARKS': 'Legal and Regulatory Offenses',
        'DEFENCE FORCES OFFENCES RELATING TO (also relating to desertion)': 'Legal and Regulatory Offenses',
        'Giving false information respecting an offence com': 'Legal and Regulatory Offenses',
        'UNNATURAL DEATH (Sec 174/174c/176)': 'Legal and Regulatory Offenses',
        'CINEMATOGRAPH ACT 1952': 'Legal and Regulatory Offenses',
        'INFANTICIDE': 'Legal and Regulatory Offenses',
        'PREVENTION OF CORRUPTION ACT 1988': 'Legal and Regulatory Offenses',
        'NATIONAL SECURITY ACT': 'Legal and Regulatory Offenses',
        'ILLEGAL DETENTION': 'Legal and Regulatory Offenses',
        'RAPE': 'Sexual Crimes',
        'IMMORAL TRAFFIC': 'Sexual Crimes',
        'SCHEDULED CASTE AND THE SCHEDULED TRIBES ': 'Hate Crimes and Discrimination',
        'COMMUNAL / RELIGION   ': 'Hate Crimes and Discrimination',
        'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)': 'Crimes Against Public Servants',
        'SUICIDE': 'Other Crimes',
        'Failure to appear to Court': 'Other Crimes',
        'ELECTION': 'Other Crimes',
        'Disobedience to Order Promulgated by PublicServan': 'Other Crimes',
        'CHILDREN ACT': 'Other Crimes',
        'ANIMAL': 'Other Crimes',
        'FOREIGNER': 'Other Crimes',
        'Attempting to commit offences': 'Other Crimes',
        'FALSE EVIDENCE': 'Other Crimes',
        'CONSUMER': 'Other Crimes',
        'DEFAMATION': 'Other Crimes',
        'ESCAPE FROM LAWFUL CUSTODY AND RESISTANCE': 'Other Crimes',
        'DEATHS-MISCARRIAGE': 'Other Crimes'
    }


    # Assuming your data is in a DataFrame called 'data'
    clean_data['Crime Group'] = clean_data['CrimeGroup_Name'].map(category_mapping)

    clean_data.drop("CrimeGroup_Name", axis = 1, inplace = True)
    return clean_data

# Function to extract numerical parts from a string
def extract_numerical_part(s):
    numerical_parts = re.findall(r'\d+', s)
    if numerical_parts:
        return ''.join(numerical_parts)
    else:
        return s


def crime_weights_calculation(clean_data):
    # Define the Crime Severity Weights mapping
    crime_severity_weights = {
        'Violent Crimes': 5,
        'Sexual Crimes': 5,
        'Crimes Against Public Servants': 4,
        'Cyber Crimes': 4,
        'Hate Crimes and Discrimination': 4,
        'Accidents and Public Safety': 3,
        'Property Crimes': 3,
        'Missing Persons': 2,
        'Legal and Regulatory Offenses': 2,
        'Other Crimes': 1
    }

    # Map the Crime Severity Weights to the Crime Category feature to create a new feature
    clean_data['Crime Severity Weights'] = clean_data['Crime Group'].map(crime_severity_weights)
    clean_data.drop("Crime Group", axis =1, inplace = True)



def police_resource_creation(clean_data):
    sanction_strength = {
    "COP, BANGALORE CITY": {"ASI": 1558, "CHC": 4650, "CPC": 9432},
    "COP, MYSORE CITY": {"ASI": 198, "CHC": 592, "CPC": 1159},
    "COP, HUBLI-DHARWAD CITY": {"ASI": 190, "CHC": 462, "CPC": 958},
    "COP, MANGALORE CITY": {"ASI": 131, "CHC": 375, "CPC": 801},
    "COP, BELGAUM CITY": {"ASI": 114, "CHC": 320, "CPC": 699},
    "COP, KALBURGI CITY": {"ASI": 81, "CHC": 223, "CPC": 556},
    "IGP, C R, BANGALOE": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, BANGALORE": {"ASI": 128, "CHC": 381, "CPC": 743},
    "SP, TUMKURU": {"ASI": 165, "CHC": 492, "CPC": 957},
    "SP, KOLAR": {"ASI": 68, "CHC": 199, "CPC": 394},
    "SP, KGF": {"ASI": 51, "CHC": 146, "CPC": 303},
    "SP, RAMANAGARA": {"ASI": 103, "CHC": 293, "CPC": 589},
    "SP, CHICKBALLAPURA": {"ASI": 88, "CHC": 258, "CPC": 529},
    "IGP, S.R, BANGALOE": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, MYSORE": {"ASI": 112, "CHC": 323, "CPC": 634},
    "SP, CHAMARAJANAGARA": {"ASI": 91, "CHC": 254, "CPC": 529},
    "SP, HASSAN": {"ASI": 132, "CHC": 382, "CPC": 749},
    "SP, KODAGU": {"ASI": 90, "CHC": 241, "CPC": 492},
    "SP, MANDYA": {"ASI": 135, "CHC": 414, "CPC": 755},
    "IGP, E.R, DAVANAGERE": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, DAVANGERE": {"ASI": 113, "CHC": 338, "CPC": 644},
    "SP, SHIVAMOGA": {"ASI": 158, "CHC": 454, "CPC": 915},
    "SP, CHITRADURGA": {"ASI": 122, "CHC": 364, "CPC": 704},
    "SP, HAVERI": {"ASI": 98, "CHC": 290, "CPC": 573},
    "IGP, W.R, MANGALORE": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, DK, MANGALORE": {"ASI": 76, "CHC": 216, "CPC": 470},
    "SP, UDUPI": {"ASI": 94, "CHC": 276, "CPC": 553},
    "SP, UK, KARWAR": {"ASI": 149, "CHC": 407, "CPC": 810},
    "SP, CHICKMAGALURU": {"ASI": 117, "CHC": 349, "CPC": 682},
    "IGP, N.R , BELGAUM": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, BELGAUM": {"ASI": 149, "CHC": 440, "CPC": 854},
    "SP, GADAG": {"ASI": 71, "CHC": 210, "CPC": 420},
    "SP, DHARWAD": {"ASI": 52, "CHC": 141, "CPC": 278},
    "SP, VIJAYAPURA": {"ASI": 133, "CHC": 413, "CPC": 835},
    "SP, BAGALKOTE": {"ASI": 111, "CHC": 331, "CPC": 660},
    "IGP, NER, KALBURGI": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, KALABURGI": {"ASI": 121, "CHC": 376, "CPC": 685},
    "SP, BIDAR": {"ASI": 148, "CHC": 442, "CPC": 870},
    "SP, YADAGIRI": {"ASI": 67, "CHC": 201, "CPC": 414},
    "IGP, BELLARI RANGE": {"ASI": 0, "CHC": 0, "CPC": 0},
    "SP, RAICHUR": {"ASI": 124, "CHC": 371, "CPC": 728},
    "SP, KOPPAL": {"ASI": 77, "CHC": 229, "CPC": 447},
    "SP, BELLARY": {"ASI": 98, "CHC": 286, "CPC": 535},
    "SP, VIJAYANAGARA": {"ASI": 114, "CHC": 303, "CPC": 598},
    "SP, RAILWAYS": {"ASI": 86, "CHC": 245, "CPC": 520}
}


    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(sanction_strength, orient='index')

    # Reset the index to make 'NAME OF THE UNITS' a column
    df.reset_index(inplace=True)

    # Rename the columns
    df.columns = ['UNITS', 'ASI', 'CHC', 'CPC']

    # Assuming you want to drop rows where "UNITS" matches specific values
    units_to_drop = ["IGP, C R, BANGALOE", "IGP, S.R, BANGALOE", "IGP, E.R, DAVANAGERE",
                    "IGP, W.R, MANGALORE", "IGP, N.R , BELGAUM", "IGP, NER, KALBURGI",
                    "IGP, BELLARI RANGE", "COP, MYSORE CITY", "SP, MYSORE", ]

    # Create a boolean mask to identify rows where "UNITS" is in units_to_drop
    mask = df["UNITS"].isin(units_to_drop)

    # Drop rows based on the mask inplace
    df.drop(df[mask].index, inplace=True)

    map = {"COP, MYSORE CITY": "Mysuru", "SP, MYSORE":"Mysuru", "SP, DK, MANGALORE": "Dakshina Kannada", "COP, MANGALORE CITY": "Dakshina Kannada", "COP, BELGAUM CITY": "Belagavi", "SP, BELGAUM": "Belagavi"}

    df["UNITS"]  = df["UNITS"].replace(map)

    districts_to_drop = ["Davanagere"]

    optimisation = clean_data[~clean_data["District_Name"].isin(districts_to_drop)]
    replace_map = {"Bagalkote": "SP, BAGALKOTE", "Ballari":"SP, BELLARY",'Bengaluru Urban': "COP, BANGALORE CITY", "Bengaluru Rural": "SP, BANGALORE", "Bidar": "SP, BIDAR", "Chamarajanagara":"SP, CHAMARAJANAGARA", "Chikkaballapura":"SP, CHICKBALLAPURA", "Chikmagalur":"SP, CHICKMAGALURU", "Chitradurga": "SP, CHITRADURGA", "Udupi":"SP, UDUPI", "Dharwad": "SP, DHARWAD", "Gadag": "SP, GADAG", "Hassan": "SP, HASSAN", "Haveri": "SP, HAVERI", "Kolar": "SP, KOLAR", "Kalaburagi": "SP, KALABURGI", "Kodagu": "SP,  KODAGU", "Koppal": "SP, KOPPAL", "Mandya":"SP, MANDYA", "Raichur":"SP, RAICHUR", "Ramanagara":"SP, RAMANAGARA", "Shimoga":"SP, SHIVAMOGA", "Tumakuru":"SP, TUMKURU", "Vijayapura":"SP, VIJAYAPURA", "Yadgir": "SP, YADAGIRI", "Uttara Kannada":"SP, UK, KARWAR"}

    optimisation["UNITS"] = optimisation["District_Name"].replace(replace_map)
    optimisation.drop_duplicates(inplace = True)
    optimisation = pd.merge(optimisation, df, on = "UNITS", how = "inner")
    print("Optimisation sample observations", optimisation.head())
    group_weight = optimisation.groupby(["Beat Number", "UnitName"])["Crime Severity Weights"].sum().reset_index()
    print("Group Weight", group_weight.head())
    optimisation.drop(columns = ["Crime Severity Weights"], axis =1, inplace = True)
    optimisation = pd.merge(optimisation,group_weight, on = ["Beat Number","UnitName"], how = "inner")
    print("optimisation after merging with group weights",optimisation.head(5))

    optimisation.drop_duplicates(subset =["UnitName", "Beat Number"], inplace = True)
    optimisation.drop(columns = ["UnitName", "District_Name"], inplace = True)
    optimisation.rename(columns = {"Crime Severity Weights": "Crime Severity Weights of Beat"}, inplace = True)
    optimisation.reset_index(inplace = True)

    return optimisation



# Function to process the dataset
def feature_engineering_resources(clean_data):
    new_feature_values = []
    for index, row in clean_data.iterrows():
        numerical_part = extract_numerical_part(str(row['Beat_Name']))
        new_feature_values.append(numerical_part)
    clean_data['Beat Number'] = new_feature_values
    clean_data.drop("Beat_Name", axis = 1, inplace = True)
    crime_weights_calculation(clean_data)
    crime_counts = clean_data.groupby(["UnitName", "Beat Number"]).size().reset_index(name = "No of Crimes in Each Beat")
    # Merge the calculated crime counts back into the original DataFrame
    resource_allocation_cleaned = pd.merge(clean_data, crime_counts, on=['UnitName', 'Beat Number'], how='left')
    resource_allocation_cleaned.drop_duplicates(inplace = True)
    optimisation = police_resource_creation(resource_allocation_cleaned)
    optimisation.drop_duplicates(inplace = True)

    # Save the new dataset to a new CSV file
    optimisation.to_csv("../Component_datasets/Resource_Allocation_Cleaned.csv", index = False)
















