import streamlit as st
import pandas as pd
import os
import sys
import datetime
import calendar
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from Continuous_learning_and_feedback.feedback import send_feedback_session_invitation
from Continuous_learning_and_feedback.alert import send_alert


def update_police_allocation():

    with st.expander("**Update Police Resources**",expanded=False):
        st.subheader("Police Resource Allocation Updation")

        # Ask user if they want to update the resource allocation
        update_needed = st.checkbox("Do you want to update the police resource allocation?")

        if update_needed:
            data_file_path = os.path.join(root_dir, 'Component_datasets', 'Resource_Allocation_Cleaned.csv')
            df = pd.read_csv(data_file_path)
            # Get the list of units
            units = df["District Name"].unique()

            # Ask user to select the unit they want to update
            selected_unit = st.selectbox("Select the unit you want to update:", units)

            # Get the current allocation for the selected unit
            current_allocation = df[df["District Name"] == selected_unit]
            current_asi = current_allocation["Sanctioned Strength of Assistant Sub-Inspectors per District"].iloc[0]
            current_chc = current_allocation["Sanctioned Strength of Head Constables per District"].iloc[0]
            current_cpc = current_allocation["Sanctioned Strength of Police Constables per District"].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Current Police Resource Allocation")
                data = {"Unit": [selected_unit], "ASI": [current_asi], "CHC": [current_chc], "CPC": [current_cpc]}
                existing_df = pd.DataFrame(data)
                st.table(existing_df)

            with col2:
                st.subheader("Update Police Resource Allocation")
                new_asi = st.number_input(f"Enter the new ASI count for {selected_unit}", min_value=int(0.7*current_asi), max_value=int(1.5*current_asi), step=1, value=int(current_asi))
                new_chc = st.number_input(f"Enter the new CHC count for {selected_unit}", min_value=int(0.7*current_chc), max_value=int(1.5*current_chc), step=1, value=int(current_chc))
                new_cpc = st.number_input(f"Enter the new CPC count for {selected_unit}", min_value=int(0.7*current_cpc), max_value=int(1.5*current_cpc), step=1, value=int(current_cpc))
                confirm_update = st.button(f"Confirm Update for {selected_unit}")




            if confirm_update:
                # Update the dataframe with the new values
                df.loc[df["District Name"] == selected_unit, "Sanctioned Strength of Assistant Sub-Inspectors per District"] = new_asi
                df.loc[df["District Name"] == selected_unit, "Sanctioned Strength of Head Constables per District"] = new_chc
                df.loc[df["District Name"] == selected_unit, "Sanctioned Strength of Police Constables per District"] = new_cpc

                st.success(f"Police resource allocation for {selected_unit} has been updated.")



def display_alert_meter(avg_rating, negative_feedback_count):
    with st.expander("**Live Feedback Monitoring and Alert Meter**", expanded=False):
        rating_threshold = 3.5
        negative_feedback_threshold = 20

        rating_percentage = (avg_rating / rating_threshold) 
        negative_feedback_percentage = (negative_feedback_count / negative_feedback_threshold) 

        st.subheader("Alert Meter")
        col1, col2 = st.columns(2)

        with col1:
            st.progress(rating_percentage, text=f"Avg. Rating: {avg_rating:.2f}")
        with col2:
            st.progress(negative_feedback_percentage, text=f"Negative Feedback: {negative_feedback_count}/{negative_feedback_threshold}")

        if rating_percentage >= 1.0 or negative_feedback_percentage >= 0.9:
            st.warning("The system is approaching the alert threshold. Please review the user feedback.")
            send_alert(avg_rating, rating_threshold, negative_feedback_count, negative_feedback_threshold)
        else:
            st.success("The system is performing well based on the user feedback.")
        
        st.markdown("**Note:** When the alert meter bars gets fulled, automatic e-mail alert reports will be sent to the technical lead to resolve the issue")

def continuous_learning_and_feedback():
    st.title("Continuous Learning and Feedback")

    st.text("Explore all the options below:")

    
    update_police_allocation()

    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Feedback.csv')
    feedback_data = pd.read_csv(data_file_path)

    avg_rating = feedback_data["Feedback Rating"].mean()
    negative_feedback_count = len(feedback_data[feedback_data["Feedback Rating"] < 3])

    display_alert_meter(avg_rating, negative_feedback_count)

    # User Feedback Mechanism
    with st.expander("**Provide Feedback**", expanded=False):
        feedback_form = st.form(key="feedback_form")
        feedback_type = feedback_form.selectbox("Select Feedback Type", ["Crime Pattern Analysis", "Criminal Profiling", "Predictive Modeling", "Resource Allocation"])
        feedback_rating = feedback_form.slider("Rate the accuracy and usefulness of the system's output", min_value=1, max_value=5, value=3)
        feedback_comments = feedback_form.text_area("Additional Comments")
        submit_feedback = feedback_form.form_submit_button("Submit Feedback")

        if submit_feedback:
            # Collect and store the feedback data
            feedback_data = {
                "Feedback Type": feedback_type,
                "Feedback Rating": feedback_rating,
                "Feedback Comments": feedback_comments
            }
            store_feedback_data(feedback_data)
            st.success("Thank you for your feedback!")

    # Knowledge Capture and Documentation
    with st.expander("**Knowledge Base**", expanded=False):   
        st.write("Insights and lessons learned from the continuous feedback process are documented here.")
        display_knowledge_base(feedback_data)

    # Collaborative Learning
    with st.expander("**Feedback Sessions Invitation**", expanded=False):
        organize_feedback_sessions()


    # Transparency and Explainability
    #st.subheader("Model Explanations")
    #st.write("Detailed explanations are provided for the system's predictions and recommendations.")
    # display_model_explanations(recidivism_model, crime_type_model, hotspot_model)

def store_feedback_data(feedback_data):
    # Save the feedback data to a file or database
    feedback_file_path = os.path.join(root_dir, 'Component_datasets', 'Feedback.csv')
    try:
        feedback_df = pd.read_csv(feedback_file_path)
        feedback_df = feedback_df.append(feedback_data, ignore_index=True)
        feedback_df.to_csv(feedback_file_path, index=False)
    except FileNotFoundError:
        feedback_df = pd.DataFrame([feedback_data])
        feedback_df.to_csv(feedback_file_path, index=False)

def display_knowledge_base(feedback_data):
    # Load and display the knowledge base document
    st.table(feedback_data)

def organize_feedback_sessions():
    st.markdown("### Organize Feedback Sessions")

    # Get user input for feedback session details
    session_date = st.date_input("Select Feedback Session Date")
    session_time = st.time_input("Select Feedback Session Time")

    # Display stakeholder management interface
    st.subheader("Manage Stakeholders")
    stakeholders = get_stakeholder_contact_info()
    stakeholder_table = st.dataframe(stakeholders)

    if "stakeholders" not in st.session_state:
        st.session_state.stakeholders = stakeholders

    # Allow user to add, edit, or remove stakeholders
    new_stakeholder_name = st.text_input("Add New Stakeholder Name")
    new_stakeholder_position = st.text_input("Add New Stakeholder's Position")
    new_stakeholder_email = st.text_input("Add New Stakeholder Email")
    if st.button("Add Stakeholder"):
        st.session_state.stakeholders.append({"name": new_stakeholder_name, "Position": new_stakeholder_position, "email": new_stakeholder_email})
        stakeholder_table.dataframe(st.session_state.stakeholders)
        st.dataframe(st.session_state.stakeholders)


    # Allow user to select stakeholders to invite
    selected_stakeholders = st.multiselect("Select Stakeholders to Invite", [s["name"] for s in st.session_state.stakeholders])

    st.markdown("**Note**: After selecting the stakeholders for invitation, click outside the dropdown menu or press the 'Esc' key to close the dropdown.")
    # Send feedback session invitation
    if st.button("Send Invitation mail"):
        # Initialize an empty list to collect email addresses
        email_addresses = []

        # Iterate over each stakeholder dictionary
        for stakeholder in st.session_state.stakeholders:
            # Extract the email address from the current stakeholder dictionary
            email_addresses.append(stakeholder["email"])

        send_feedback_session_invitation(session_date, session_time, email_addresses)



# def get_next_feedback_session_date():
#     # Set the feedback session to be held on the first Monday of the month
#     target_weekday = calendar.MONDAY
#     now = datetime.datetime.now()
#     days_until_target = (target_weekday - now.weekday()) % 7
#     next_session_date = now + datetime.timedelta(days=days_until_target)
#     return next_session_date

def get_stakeholder_contact_info():
    # Retrieve the list of stakeholders and their contact information (e.g., from a database or a CSV file)
    stakeholders = [
        {"name": "Vishal",  "Position": "Technical Lead", "email": "vishalkumars.work@gmail.com"},
    ]
    return stakeholders


# def display_model_explanations(recidivism_model, crime_type_model, hotspot_model):
#     # Provide detailed explanations for the predictions and recommendations of the models
#     display_recidivism_model_explanations(recidivism_model)
#     display_crime_type_model_explanations(crime_type_model)
#     display_hotspot_model_explanations(hotspot_model)








