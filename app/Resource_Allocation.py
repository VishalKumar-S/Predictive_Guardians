import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from pulp import LpVariable, LpProblem, LpMinimize, lpSum, value

import pandas as pd
from pulp import LpVariable, LpProblem, LpMinimize, lpSum, value

def optimize_police_allocation(optimisation, unit_name, a=0.5, b=2, r1=0.3, r2=0.5):
    # Filter data based on the selected unit
    filtered_data = optimisation[optimisation['UNITS'] == unit_name]


    # Sort DataFrame by weighted_score in descending order
    filtered_data = filtered_data.sort_values(by=['Crime Severity Weights of Beat', 'No of Crimes in Each Beat'], ascending=False)

    if filtered_data.empty:
        print(f"No data found for the selected unit: {unit_name}")
        return

    # Extract relevant features
    num_beats = len(filtered_data)
    total_asi = filtered_data['ASI'].iloc[0]
    total_chc = filtered_data['CHC'].iloc[0]
    total_cpc = filtered_data['CPC'].iloc[0]
    beat_names = filtered_data['Beat Number'].tolist()
    village_names = filtered_data['Village_Area_Name'].tolist()
    station_names = filtered_data['UNITS'].tolist()
    no_of_crimes = filtered_data['No of Crimes in Each Beat'].tolist()
    crime_severity_weights = filtered_data['Crime Severity Weights of Beat'].tolist()




    # Create optimization model
    model = LpProblem(name="Police_Allocation_Optimization", sense=LpMinimize)

    # Decision variables: ASI, CHC, CPC officers per beat
    asi = [LpVariable(name=f"ASI_{i}", lowBound=0, upBound=total_asi, cat='Integer') for i in range(num_beats)]
    chc = [LpVariable(name=f"CHC_{i}", lowBound=0, upBound=total_chc, cat='Integer') for i in range(num_beats)]
    cpc = [LpVariable(name=f"CPC_{i}", lowBound=0, upBound=total_cpc, cat='Integer') for i in range(num_beats)]

    # Objective function: Minimize the maximum unmet demand across all beats
    model += lpSum(max(1, a * int(no_of_crimes[i] ** 0.5) + b) - (asi[i] + chc[i] + cpc[i]) for i in range(num_beats))

    # Constraints
    # Total officers constraint
    model += lpSum(asi) <= total_asi
    model += lpSum(chc) <= total_chc
    model += lpSum(cpc) <= total_cpc

    max_officers_per_beat = 10
    # Minimum and maximum officers per beat constraint
    for i in range(num_beats):
        model += asi[i] + chc[i] + cpc[i] <= max_officers_per_beat
        model += asi[i] + chc[i] + cpc[i] >= 2
        model += asi[i] <=1


    # Officer type ratio constraint
    for i in range(num_beats):
        # Define the total number of non-ASI officers (CHC + CPC)
        non_asi_officers = chc[i] + cpc[i]

        # Add the constraint for ASI officers ratio
        #model += asi[i] <= r1 * non_asi_officers

        # Add the constraint for CHC officers ratio with CPC officers
        model += chc[i] <= r2 * cpc[i]



    # Solve the optimization problem
    try:
        model.solve()
    except Exception as e:
        print(f"Error occurred during optimization: {e}")
        return

    # Output optimal allocation results
    print(f"Optimal Police Resource Allocation for {unit_name}:")
    print(f"Total no of officers in {unit_name} is ASI:{total_asi}, CHC: {total_chc}, CPC: {total_cpc}")
    # for i in range(num_beats):
    #     print(f"Beat {beat_names[i]}: ASI={int(value(asi[i]))}, CHC={int(value(chc[i]))}, CPC={int(value(cpc[i]))}, crime severity of beat = {crime_severity_weights[i]}, no of crimes = {no_of_crimes[i]}")





    asi_sum = sum(int(value(asi[i])) for i in range(num_beats))
    chc_sum = sum(int(value(chc[i])) for i in range(num_beats))
    cpc_sum = sum(int(value(cpc[i])) for i in range(num_beats))

    return num_beats, asi_sum, chc_sum, cpc_sum, beat_names, village_names, station_names,asi, chc, cpc, crime_severity_weights, no_of_crimes


def display_police_allocation(num_beats, unit_name, asi_sum, chc_sum, cpc_sum, beat_names, village_names, station_names, asi, chc, cpc, crime_severity_weights, no_of_crimes):
    st.subheader(f"Police Resource Allocation for {unit_name}")
    st.write(f"Total no of ASSISTANT Sub Inspectors in {unit_name} is {asi_sum}")
    st.write(f"Total no of Head Constables in {unit_name} is {chc_sum}")
    st.write(f"Total no of Police Constables in {unit_name} is {cpc_sum}")

    st.write("Optimal Police Resource Allocation")
    data = {
        "Police Station": station_names,
        "Area name": village_names,
        "Beat Number": beat_names,
        "ASI": [int(value.value()) for value in asi],
        "CHC": [int(value.value()) for value in chc],
        "CPC": [int(value.value()) for value in cpc],
        "Crime Severity of Beat": [crime_severity_weights[i] for i in range(num_beats)],
        "No of Previous Crimes": [no_of_crimes[i] for i in range(num_beats)]
    }

    df = pd.DataFrame(data)
    st.table(df)

def resource_allocation(df):
    st.title("Police Resource Allocation and Suggestions")
    options = ["Select an Unit"] + list(df["UNITS"].unique())
    option = st.selectbox("Select an option", options)

    if option != "Select an Unit":
        unit_name = option
        num_beats, asi_sum, chc_sum, cpc_sum, beat_names,village_names, station_names, asi, chc, cpc, crime_severity_weights, no_of_crimes = optimize_police_allocation(df, unit_name)
        display_police_allocation(num_beats, unit_name, asi_sum, chc_sum, cpc_sum, beat_names, village_names, station_names, asi, chc, cpc, crime_severity_weights, no_of_crimes)



