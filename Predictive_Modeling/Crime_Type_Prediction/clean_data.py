import pandas as pd

def clean_Crime_type_data(clean_data):
    clean_data = clean_data.reset_index(drop=True)
    clean_data = clean_data[~((clean_data["Latitude"] > 19) |
                                (clean_data["Longitude"] > 78) |
                                (clean_data["Latitude"] < 11) |
                                (clean_data["Longitude"] < 74))]


    clean_data =clean_data[['District_Name', 'Offence_From_Date', 'Offence_To_Date', 'CrimeGroup_Name']]

    clean_data.drop_duplicates(inplace = True)

    clean_data.dropna(inplace = True)

    new_category_mapping = {
        'THEFT': 'PROPERTY CRIMES',
        'MOTOR VEHICLE ACCIDENTS NON-FATAL': 'TRAFFIC OFFENSES',
        'MISSING PERSON': 'MISSING PERSONS AND KIDNAPPING',
        'CYBER CRIME': 'CYBERCRIME AND FRAUD',
        'CASES OF HURT': 'VIOLENT CRIMES',
        'CrPC': 'OTHER OFFENSES',
        'PUBLIC SAFETY': 'PUBLIC SAFETY OFFENSES',
        'KARNATAKA POLICE ACT 1963': 'OTHER OFFENSES',
        'CHEATING': 'CYBERCRIME AND FRAUD',
        'MOTOR VEHICLE ACCIDENTS FATAL': 'TRAFFIC OFFENSES',
        'Karnataka State Local Act': 'OTHER OFFENSES',
        'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES': 'DRUG OFFENSES',
        'NEGLIGENT ACT': 'NEGLIGENCE AND RASH ACTS',
        'BURGLARY - NIGHT': 'PROPERTY CRIMES',
        'MOLESTATION': 'CRIMES AGAINST WOMEN',
        'KIDNAPPING AND ABDUCTION': 'MISSING PERSONS AND KIDNAPPING',
        'RIOTS': 'PUBLIC SAFETY OFFENSES',
        'ATTEMPT TO MURDER': 'VIOLENT CRIMES',
        'ROBBERY': 'PROPERTY CRIMES',
        'CRUELTY BY HUSBAND': 'CRIMES AGAINST WOMEN',
        'CRIMES RELATED TO WOMEN': 'CRIMES AGAINST WOMEN',
        'POCSO': 'CRIMES AGAINST CHILDREN',
        'CRIMINAL INTIMIDATION': 'VIOLENT CRIMES',
        'CRIMINAL TRESPASS': 'PROPERTY CRIMES',
        'MURDER': 'VIOLENT CRIMES',
        'BURGLARY - DAY': 'PROPERTY CRIMES',
        'SCHEDULED CASTE AND THE SCHEDULED TRIBES': 'HATE CRIMES',
        'DACOITY': 'VIOLENT CRIMES',
        'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)': 'CRIMES AGAINST PUBLIC SERVANTS',
        'COTPA, CIGARETTES AND OTHER TOBACCO PRODUCTS': 'OTHER OFFENSES',
        'SUICIDE': 'OTHER OFFENSES',
        'CRIMINAL BREACH OF TRUST': 'CYBERCRIME AND FRAUD',
        'RAPE': 'CRIMES AGAINST WOMEN',
        'DEATHS DUE TO RASHNESS/NEGLIGENCE': 'NEGLIGENCE AND RASH ACTS',
        'MISCHIEF': 'OTHER OFFENSES',
        'CONSUMER': 'OTHER OFFENSES',
        'FORGERY': 'CYBERCRIME AND FRAUD',
        'IMMORAL TRAFFIC': 'CRIMES AGAINST WOMEN',
        'Failure to appear to Court': 'OTHER OFFENSES',
        'COPY RIGHT ACT 1957': 'INTELLECTUAL PROPERTY OFFENSES',
        'AFFRAY': 'PUBLIC SAFETY OFFENSES',
        'ARSON': 'PROPERTY CRIMES',
        'WRONGFUL RESTRAINT/CONFINEMENT': 'VIOLENT CRIMES',
        'ELECTION': 'OTHER OFFENSES',
        'Disobedience to Order Promulgated by PublicServan': 'OTHER OFFENSES',
        'CHILDREN ACT': 'CRIMES AGAINST CHILDREN',
        'ARMS ACT  1959': 'OTHER OFFENSES',
        'ANIMAL': 'OTHER OFFENSES',
        ' PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984': 'PUBLIC SAFETY OFFENSES',
        'DOWRY DEATHS': 'CRIMES AGAINST WOMEN',
        'COMMUNAL / RELIGION': 'HATE CRIMES',
        'INSULTING MODESTY OF WOMEN (EVE TEASING)': 'CRIMES AGAINST WOMEN',
        ' REPRESENTATION OF PEOPLE ACT 1951 & 1988': 'OTHER OFFENSES',
        'FOREIGNER': 'OTHER OFFENSES',
        'EXPOSURE AND ABANDONMENT OF CHILD': 'CRIMES AGAINST CHILDREN',
        'Attempting to commit offences': 'OTHER OFFENSES',
        'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'VIOLENT CRIMES',
        'EXPLOSIVES': 'PUBLIC SAFETY OFFENSES',
        'OFFENCES PROMOTING ENEMITY': 'HATE CRIMES',
        'PUBLIC NUISANCE': 'OTHER OFFENSES',
        'Concealment of birth by secret disposal of Child': 'CRIMES AGAINST CHILDREN',
        'PASSPORT ACT': 'OTHER OFFENSES',
        'ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'VIOLENT CRIMES',
        'OFFENCES RELATED TO MARRIAGE': 'OTHER OFFENSES',
        'COUNTERFEITING': 'CYBERCRIME AND FRAUD',
        'ESCAPE FROM LAWFUL CUSTODY AND RESISTANCE': 'OTHER OFFENSES',
        'ASSAULT': 'VIOLENT CRIMES',
        'CRIMINAL CONSPIRACY': 'OTHER OFFENSES',
        'FALSE EVIDENCE': 'OTHER OFFENSES',
        'PORNOGRAPHY': 'OTHER OFFENSES',
        'ADULTERATION': 'OTHER OFFENSES',
        'POISONING-PROFESSIONAL': 'OTHER OFFENSES',
        'SLAVERY': 'HATE CRIMES',
        'OFFENCES BY PUBLIC SERVANTS (EXCEPT CORRUPTION) (Public servant is accused)': 'CRIMES AGAINST PUBLIC SERVANTS',
        'DEATHS-MISCARRIAGE': 'OTHER OFFENSES',
        'CRIMINAL MISAPPROPRIATION': 'OTHER OFFENSES',
        'BONDED LABOUR SYSTEM': 'HATE CRIMES',
        'FOREST': 'OTHER OFFENSES',
        'INDIAN ELECTRICITY ACT': 'OTHER OFFENSES',
        'DEFAMATION': 'OTHER OFFENSES',
        'INDIAN MOTOR VEHICLE': 'TRAFFIC OFFENSES',
        'UNNATURAL SEX': 'OTHER OFFENSES',
        'IMPERSONATION': 'OTHER OFFENSES',
        'PUBLIC JUSTICE': 'OTHER OFFENSES',
        'OF ABETMENT': 'OTHER OFFENSES',
        'ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN': 'CRIMES AGAINST WOMEN',
        ' POST & TELEGRAPH,TELEGRAPH WIRES(UNLAWFUL POSSESSION)ACT 1950': 'OTHER OFFENSES',
        'Human Trafficking': 'CRIMES AGAINST WOMEN',
        'ANTIQUES (CULTURAL PROPERTY)': 'OTHER OFFENSES',
        'OFFICIAL SECURITY RELATED ACTS': 'PUBLIC SAFETY OFFENSES',
        'UNLAWFUL ACTIVITIES(Prevention)ACT 1967': 'PUBLIC SAFETY OFFENSES',
        'SEDITION': 'PUBLIC SAFETY OFFENSES',
        'RECEIVING OF STOLEN PROPERTY': 'PROPERTY CRIMES',
        'DOCUMENTS & PROPERTY MARKS': 'OTHER OFFENSES',
        'DEFENCE FORCES OFFENCES RELATING TO (also relating to desertion)': 'OTHER OFFENSES',
        'Giving false information respecting an offence com': 'OTHER OFFENSES',
        'UNNATURAL DEATH (Sec 174/174c/176)': 'OTHER OFFENSES',
        'CINEMATOGRAPH ACT 1952': 'OTHER OFFENSES',
        'INFANTICIDE': 'CRIMES AGAINST CHILDREN',
        'PREVENTION OF CORRUPTION ACT 1988': 'OTHER OFFENSES',
        'NATIONAL SECURITY ACT': 'PUBLIC SAFETY OFFENSES',
        'ILLEGAL DETENTION': 'OTHER OFFENSES'
    }

    # Map the existing crime categories to the new broader categories
    clean_data['Crime Category'] = clean_data['CrimeGroup_Name'].map(new_category_mapping)

    
    # Convert 'Offence_From_Date' and 'Offence_To_Date' columns to datetime
    clean_data['Offence_From_Date'] = pd.to_datetime(clean_data['Offence_From_Date'])
    clean_data['Offence_To_Date'] = pd.to_datetime(clean_data['Offence_To_Date'])

    # Create new features from 'Offence_From_Date'
    clean_data['Offence_From_Year'] = clean_data['Offence_From_Date'].dt.year
    clean_data['Offence_From_Month'] = clean_data['Offence_From_Date'].dt.month
    clean_data['Offence_From_Day'] = clean_data['Offence_From_Date'].dt.day

    # Create new features from 'Offence_To_Date'
    clean_data['Offence_To_Year'] = clean_data['Offence_To_Date'].dt.year
    clean_data['Offence_To_Month'] = clean_data['Offence_To_Date'].dt.month
    clean_data['Offence_To_Day'] = clean_data['Offence_To_Date'].dt.day

    clean_data.drop(["Offence_From_Date", "Offence_To_Date"], axis =1,inplace = True)

    clean_data.drop_duplicates(inplace = True)
    clean_data.dropna(inplace = True)
    clean_data.drop(columns = ["CrimeGroup_Name"], inplace = True)

    clean_data.to_csv("../Component_datasets/Crime_Type_cleaned_data.csv")

    return clean_data



