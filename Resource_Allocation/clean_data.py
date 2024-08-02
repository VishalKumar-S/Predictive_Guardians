import numpy as np
import pandas as pd


def clean_resource_data(df):
    df["Total Crimes per beat"] = df.groupby(["District_Name", "UnitName", "Village_Area_Name", "Beat_Name"])["FIRNo"].transform("count")

    df = df[(df["District_Name"]!= "CID") & (df["District_Name"]!= "ISD Bengaluru") & (df["District_Name"]!= "Coastal Security Police")]

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

    district_mapping = {
    'Bagalkot': 'SP, BAGALKOTE',
    'Ballari': 'SP, BELLARY',
    'Belagavi City': 'COP, BELGAUM CITY',
    'Belagavi Dist': 'SP, BELGAUM',
    'Bengaluru City': 'COP, BANGALORE CITY',
    'Bengaluru Dist': 'SP, BANGALORE',
    'Bidar': 'SP, BIDAR',
    'Chamarajanagar': 'SP, CHAMARAJANAGARA',
    'Chickballapura': 'SP, CHICKBALLAPURA',
    'Chikkamagaluru': 'SP, CHICKMAGALURU',
    'Chitradurga': 'SP, CHITRADURGA',
    'Dakshina Kannada': 'SP, DK, MANGALORE',
    'Davanagere': 'SP, DAVANGERE',
    'Dharwad': 'SP, DHARWAD',
    'Gadag': 'SP, GADAG',
    'Hassan': 'SP, HASSAN',
    'Haveri': 'SP, HAVERI',
    'Hubballi Dharwad City': 'COP, HUBLI-DHARWAD CITY',
    'K.G.F': 'SP, KGF',
    'Kalaburagi': 'SP, KALABURGI',
    'Kalaburagi City': 'COP, KALBURGI CITY',
    'Karnataka Railways': 'SP, RAILWAYS',
    'Kodagu': 'SP, KODAGU',
    'Kolar': 'SP, KOLAR',
    'Koppal': 'SP, KOPPAL',
    'Mandya': 'SP, MANDYA',
    'Mangaluru City': 'COP, MANGALORE CITY',
    'Mysuru City': 'COP, MYSORE CITY',
    'Mysuru Dist': 'SP, MYSORE',
    'Raichur': 'SP, RAICHUR',
    'Ramanagara': 'SP, RAMANAGARA',
    'Shivamogga': 'SP, SHIVAMOGA',
    'Tumakuru': 'SP, TUMKURU',
    'Udupi': 'SP, UDUPI',
    'Uttara Kannada': 'SP, UK, KARWAR',
    'Vijayanagara': 'SP, VIJAYANAGARA',
    'Vijayapur': 'SP, VIJAYAPURA',
    'Yadgir': 'SP, YADAGIRI'
    }

    df["District Name"] =  df["District_Name"].map(district_mapping)

    sanctioned_df = pd.DataFrame(sanction_strength).T

    df = df.merge(sanctioned_df, left_on='District Name', right_index=True, how='left')
    
    df.drop(columns = ["District_Name", "FIRNo"], inplace = True)

    df.dropna(inplace = True)
    df.drop_duplicates(inplace = True)

    
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
        'DEATHS-MISCARRIAGE': 'Other Crimes',
        'KARNATAKA POLICE ACT 1963': "Legal and Regulatory Offenses" ,
        'RAILWAYS ACT': "Legal and Regulatory Offenses",
        'OFFENCES AGAINST STATE': "Legal and Regulatory Offenses",
        'CIVIL RIGHTS ': "Hate Crimes and Discrimination",
        'FAILURE TO APPEAR TO COURT': "Other Crimes",
        'BUYING & SELLING MINOR FOR PROSTITUTION': "Sexual Crimes",
    }


    # Assuming your data is in a DataFrame called 'data'
    df['Crime Group'] = df['CrimeGroup_Name'].map(category_mapping)

    df.drop(columns = ["CrimeGroup_Name"], inplace = True)

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

    df["Crime Severity"] = df["Crime Group"].map(crime_severity_weights)

    df.drop(columns = ["Crime Group"], inplace = True)
    df.dropna(inplace = True)
    crime_severity_group = df.groupby(["District Name","UnitName","Beat_Name"]).agg(Crime_Severity_per_Beat = ("Crime Severity", "sum"))

    df = df.merge(crime_severity_group["Crime_Severity_per_Beat"], on = ["District Name","UnitName","Beat_Name"], how = "left")

    df.drop(columns = ["Crime Severity"], inplace = True)


    df.drop_duplicates(inplace = True)

    new_order = ['District Name', 'UnitName',  'Village_Area_Name', 'Beat_Name','Total Crimes per beat', 'Crime_Severity_per_Beat', 'ASI', 'CHC', 'CPC']
    df = df[new_order]

    columns_to_rename = {'UnitName': 'Police Unit',
    'Beat_Name': 'Beat Name',
    'Village_Area_Name': "Village Area Name",
    "Accused_to_Arrested": "Accused to Arrested Ratio",
    "Charge_Sheeted_to_Arrested": "Charge Sheeted to Arrested Ratio",
    "Crime_Severity_per_Beat": "Crime Severity per Beat",
    "ASI": "Sanctioned Strength of Assistant Sub-Inspectors per District",
    "CHC": "Sanctioned Strength of Head Constables per District",
    "CPC": "Sanctioned Strength of Police Constables per District"}

    df = df.rename(columns=columns_to_rename)

    columns_to_convert = ['Sanctioned Strength of Assistant Sub-Inspectors per District',
                      'Sanctioned Strength of Head Constables per District',
                      'Sanctioned Strength of Police Constables per District']

    df[columns_to_convert] = df[columns_to_convert].apply(np.round).astype(int)
    
    # Calculate the sum of 'Crime Severity per Beat' for each district
    district_crime_severity_sum = df.groupby("District Name")["Crime Severity per Beat"].sum()

    # Calculate 'Normalised Crime Severity' by dividing 'Crime Severity per Beat' by the sum for each district
    df["Normalised Crime Severity"] = df.apply(lambda row: row["Crime Severity per Beat"] / district_crime_severity_sum[row["District Name"]], axis=1)

    df.drop(columns = ["Crime Severity per Beat"], inplace = True)


    # Save the new dataset to a new CSV file
    df.to_csv("../Component_datasets/Resource_Allocation_Cleaned.csv", index = False)














