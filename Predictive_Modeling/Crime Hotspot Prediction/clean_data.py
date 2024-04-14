import numpy as np
import pandas as pd 


def clean_crime_hotspot(hotspot):

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
        'KARNATAKA POLICE ACT 1963': 'Legal and Regulatory Offenses',
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
    hotspot['Crime Group'] = hotspot['CrimeGroup_Name'].map(category_mapping)

    hotspot = hotspot.drop('CrimeGroup_Name', axis =1)

    hotspot = hotspot.drop_duplicates(subset = ["Year", "Month", "Day"])