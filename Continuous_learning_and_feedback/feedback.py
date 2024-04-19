import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import streamlit as st
import datetime

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def send_feedback_session_invitation(session_date, session_time, email_addresses):
    # Set up email details
    sender_email = "app.technicalteam@gmail.com"
    for email_address in email_addresses:
        receiver_email = email_address
        password = os.environ.get('EMAIL_PASSWORD')
        print("Password is",password)
        subject = f"Invitation: Predictive Guardians Feedback Session on {session_date.strftime('%B %d, %Y')} at {session_time.strftime('%I:%M %p')}"

        body = f"""
        Dear Stakeholder,

        You are cordially invited to the Predictive Guardians Feedback Session, which will be held on {session_date.strftime('%B %d, %Y')} at {session_time}.

        This session is an opportunity for us to gather your valuable input, discuss the system's performance, and identify areas for improvement. Your participation is crucial to the continuous enhancement of our Predictive Crime Analytics solution.

        Please let us know if you can attend the session by responding to this email.

        Best regards,
        The Predictive Guardians Team
        """

        # Specify the file path of the attachment
        attachment_path = os.path.join(root_dir, "Component_datasets", "Feedback.csv")

        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, "plain"))

        # Attach the file
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            message.attach(part)

        # Send the email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(message)
                logging.info("E-mail invitation sent successfully")
                st.success(f"Feedback session invitation email ✉️ have been sent to the {email_address}.")
                st.warning("📬 Haven't received the email invitation? Check your spam folder for any missed messages!")

        except Exception as e:
                logging.error(f"Error sending email: {e}")
                st.error("An error occurred while sending the email invitation. Please try again later.")


