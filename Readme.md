## Crime pattern analysis component:

### Join Condition for merge dataset:

Stage 1: Join FIR_Details_Data with VictimInfoDetails and ArrestPersonDetails datasets. Join Condition: on=['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'Crime_No', 'Arr_ID'] This join condition will match the records based on the common keys present in all three datasets, ensuring that we have detailed information about the FIR cases, including victim and accused details.

Stage 2: Join the result of Stage 1 with the AccusedData dataset. Join Condition: on=['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'Arr_ID'] This will add additional information about the accused individuals, such as their caste, profession, and address details.

Stage 3: Join the result of Stage 2 with the ChargsheetedDetails dataset. Join Condition: on=['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month', 'Crime_No'] This will add information about the chargesheeting process and relevant dates.



To find the correct latitude and longitude of the crime happened,
    Find the latitude and longitude values of the registered crime's police station ['UnitName'] using geocoding tool, then extract the direction and distance, adn respective distance units [KM/m/feet] from the "Distance From PS" feature using regex expressions and then perform matehmatical calcualtions to find the eaxact crime location from the known police station co-ordinated and update the new crime's latitude and longitude values. Outliers also handled here.

#### Temporal Analysis:
    Used Features: FIR_Reg_DateTime (year, month, day) District_Name
to Create  bar charts to visualize crime trends over time (years, months, days) for each district or crime type. Analyze seasonality and cyclic patterns and added 
Interactive Elements: Allow users to select the time granularity (year, month, day), filter by district or crime type, and explore trends using interactive tooltips.
using Plotly for interactive time-series visualizations.


## System Requirements

Before running this application, ensure that you have Java Runtime Environment (JRE) installed on your system. You can download and install JRE from [here](https://www.oracle.com/java/technologies/javase-jre8-downloads.html).
