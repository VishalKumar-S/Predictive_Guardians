import pandas as pd

df = pd.read_csv("datasets/Crime Pattern Analysis/Crime_Pattern_Analysis_Cleaned.csv")

print("initial memory", df.memory_usage(deep=True).sum() / 1024**2)

print(df.info())

pd.set_option("display.max_columns", None)
print(df.head())

crime_pattern_analysis = df.copy()


# Reduce bit depth of numeric columns to 16-bit integers
crime_pattern_analysis['Year'] = crime_pattern_analysis['Year'].astype('int16')
crime_pattern_analysis['Month'] = crime_pattern_analysis['Month'].astype('int16')
crime_pattern_analysis['VICTIM COUNT'] = crime_pattern_analysis['VICTIM COUNT'].astype('int16')
crime_pattern_analysis['Accused Count'] = crime_pattern_analysis['Accused Count'].astype('int16')
crime_pattern_analysis['Day'] = crime_pattern_analysis['Day'].astype('int16')

# Reduce bit depth of latitude and longitude columns to 32-bit floats
crime_pattern_analysis['Latitude'] = crime_pattern_analysis['Latitude'].astype('float16')
crime_pattern_analysis['Longitude'] = crime_pattern_analysis['Longitude'].astype('float16')

print("After compression memory", crime_pattern_analysis.memory_usage(deep=True).sum() / 1024**2)

print(crime_pattern_analysis.info())
crime_pattern_analysis.to_csv("datasets/Crime Pattern Analysis/Compressed.csv")


