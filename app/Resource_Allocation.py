import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from pulp import LpVariable, LpProblem, LpMaximize, lpSum, value

def optimise_resource_allocation(district_name, sanctioned_asi, sanctioned_chc, sanctioned_cpc):
    # Initialize the problem
    problem = LpProblem("Optimal_Resource_Allocation", LpMaximize)

    # Decision variables for each beat and officer type
    asi_vars = LpVariable.dicts("ASI", district_name.index, lowBound=0, cat='Integer')
    chc_vars = LpVariable.dicts("CHC", district_name.index, lowBound=0, cat='Integer')
    cpc_vars = LpVariable.dicts("CPC", district_name.index, lowBound=0, cat='Integer')

    # Objective function: Maximize the sum of weighted severity scores
    problem += lpSum(district_name.loc[i, 'Normalised Crime Severity'] * (asi_vars[i] + chc_vars[i] + cpc_vars[i]) for i in district_name.index)

    # Constraints
    # Constraint: Total officers in each district should not exceed sanctioned strength
    problem += lpSum(asi_vars[i] for i in district_name.index) <= sanctioned_asi
    problem += lpSum(chc_vars[i] for i in district_name.index) <= sanctioned_chc
    problem += lpSum(cpc_vars[i] for i in district_name.index) <= sanctioned_cpc

    # Constraint: Each beat must have at least one officer
    for i in district_name.index:
        problem += asi_vars[i] + chc_vars[i] + cpc_vars[i] >= 1

    # Constraint: Allocation based on normalized severity
    for i in district_name.index:
        problem += asi_vars[i] <= max(1, sanctioned_asi * district_name.loc[i, 'Normalised Crime Severity'])
        problem += chc_vars[i] <= max(1, sanctioned_chc * district_name.loc[i, 'Normalised Crime Severity'])
        problem += cpc_vars[i] <= max(1, sanctioned_cpc * district_name.loc[i, 'Normalised Crime Severity'])

    st.write("Calculating crime severity based on crime types and crime frequency for allocating resources accordingly...")

    # Solve the problem
    problem.solve()

    # Extract results
    district_name['Allocated ASI'] = [asi_vars[i].varValue for i in district_name.index]
    district_name['Allocated CHC'] = [chc_vars[i].varValue for i in district_name.index]
    district_name['Allocated CPC'] = [cpc_vars[i].varValue for i in district_name.index]

    columns_to_convert = ['Allocated ASI', 'Allocated CHC', 'Allocated CPC']
    district_name[columns_to_convert] = district_name[columns_to_convert].apply(np.round).astype(int)

    return district_name


def allocate_resources(option, district_name, updated_asi, updated_chc, updated_cpc):

    st.write(f"### Current sanctioned strengths for {option}:")
    st.write(f"ASI: {updated_asi}, CHC: {updated_chc}, CPC: {updated_cpc}")

    st.write("### Resource allocation in progress...")

    updated_district = optimise_resource_allocation(district_name, updated_asi, updated_chc, updated_cpc)
    
    st.write("### Allocation complete.")
    st.write("You can now view the resource allocation for specific police units.")

    police_units = ["All"] + list(district_name["Police Unit"].unique())
    selected_units = st.multiselect("Select Police Units to view allocation:", police_units)

    if "All" in selected_units:
        selected_data = updated_district
    else:
        selected_data = updated_district[updated_district["Police Unit"].isin(selected_units)]



    show = st.button("Show Allocation")
    if show:
        selected_data = selected_data.reset_index(drop=True)
        # st.table(selected_data[["Village Area Name", "Beat Name", "Normalised Crime Severity", "Allocated ASI", "Allocated CHC", "Allocated CPC"]])
        st.table(selected_data)
        st.session_state.default = False
        st.session_state.apply = False



def resource_allocation(df):
    st.title("Police Resource Allocation and Management")
    options = ["Select the District"] + list(df["District Name"].unique())
    option = st.selectbox("Select an option", options)

    if option != "Select the District":
        district_name = df[df["District Name"] == option]
        st.write(f"### Selected District: {option}")
        
        default_asi = int(district_name['Sanctioned Strength of Assistant Sub-Inspectors per District'].iloc[0])
        default_chc = int(district_name['Sanctioned Strength of Head Constables per District'].iloc[0])
        default_cpc = int(district_name['Sanctioned Strength of Police Constables per District'].iloc[0])

        sanctioned_asi = st.number_input("Sanctioned Assistant Sub-Inspectors [ASI]", value=default_asi, min_value=int(default_asi * 0.9), max_value=int(default_asi * 1.1), step=1)
        sanctioned_chc = st.number_input("Sanctioned Head Constables [CHC]", value=default_chc, min_value=int(default_chc * 0.9), max_value=int(default_chc * 1.1), step=1)
        sanctioned_cpc = st.number_input("Sanctioned Police Constables [CPC]", value=default_cpc, min_value=int(default_cpc * 0.9), max_value=int(default_cpc * 1.1), step=1)

        if "default" not in st.session_state:
            st.session_state.default = False
        
        if "apply" not in st.session_state:
            st.session_state.apply = False

        
        default = st.button("Use default sanctioned strengths")
        
        apply = st.button("Apply")

        if (default or st.session_state.default) and not st.session_state.apply :
            st.session_state.apply = False
            st.session_state.default = True
            updated_asi = default_asi
            updated_chc = default_chc
            updated_cpc = default_cpc
            allocate_resources(option, district_name, updated_asi, updated_chc, updated_cpc)



        if (apply or st.session_state.apply) and not st.session_state.default:
            st.session_state.default = False
            st.session_state.apply = True
            updated_asi = sanctioned_asi
            updated_chc = sanctioned_chc
            updated_cpc = sanctioned_cpc
            allocate_resources(option, district_name, updated_asi, updated_chc, updated_cpc)
