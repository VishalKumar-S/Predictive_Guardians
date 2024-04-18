from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import logging
import os
import streamlit as st
import pandas as pd
import requests
import base64
import os


# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))



class NotificationSender:
    def __init__(self, sender, email_addresses, password, subject, body, path):
        self.sender = sender
        self.email_addresses = email_addresses
        self.password = password
        self.subject = subject
        self.body = body
        self.path = path



    def send_email(self):
        try:
            for email_address in self.email_addresses:
                message = MIMEMultipart()
                message['From'] = self.sender
                message['To'] = email_address
                message['Subject'] = self.subject


                

                message.attach(MIMEText(self.body, "plain"))

                filename = self.path
                with open(filename, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                message.attach(part)

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(self.sender, self.password)
                    server.sendmail(self.sender, email_address, message.as_string())

                logging.info("E-mail invitation sent successfully")
                st.success(f"Feedback session invitation email ✉️ have been sent to the {email_address}.")
                st.warning("📬 Haven't received the email invitation? Check your spam folder for any missed messages!")
        
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            st.error("An error occurred while sending the email invitation. Please try again later.")



def send_feedback_session_invitation(session_date, session_time, email_addresses):
    sender = "mlopsproject612@gmail.com"
    password = os.environ.get('EMAIL_PASSWORD')
    subject = f"Invitation: Predictive Guardians Feedback Session on {session_date.strftime('%B %d, %Y')} at {session_time.strftime('%I:%M %p')}"

    
    path = os.path.join(root_dir, "Component_datasets", "Feedback.csv")

    body = f"""
    Dear Stakeholder,

    You are cordially invited to the Predictive Guardians Feedback Session, which will be held on {session_date.strftime('%B %d, %Y')} at {session_time}.

    This session is an opportunity for us to gather your valuable input, discuss the system's performance, and identify areas for improvement. Your participation is crucial to the continuous enhancement of our Predictive Crime Analytics solution.

    Please let us know if you can attend the session by responding to this email.

    Best regards,
    The Predictive Guardians Team
    """

    alert_sender = NotificationSender(sender, email_addresses, password, subject, body, path)
    alert_sender.send_email()








