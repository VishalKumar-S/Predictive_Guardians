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

                logging.info("E-mail alert sent successfully")
                st.success(f"Alert report email ✉️ have been sent to the {email_address}.")
                st.warning("📬 Haven't received the email invitation? Check your spam folder for any missed messages!")
        
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            st.error("An error occurred while sending the email invitation. Please try again later.")



def send_alert(avg_rating, rating_threshold, negative_feedback_count, negative_feedback_threshold):
    sender = "mlopsproject612@gmail.com"
    password = os.environ.get('EMAIL_PASSWORD')
    subject = f"User Feedback Alert - System Approaching Thresholds"
    email_addresses = ["vishalkumars.work@gmail.com"]
    
    path = os.path.join(root_dir, "Component_datasets", "Feedback.csv")

    body = f"""
    Dear Engineering Team,

    Our user feedback monitoring system has detected that one or more of the configured thresholds has been approached or exceeded. This automated alert is to notify you of the issue, so that you can investigate and address the underlying problems.

    The specific details are as follows:

    1. Average User Rating Threshold:
      ->Current Average Rating: {avg_rating}
      ->Threshold: {rating_threshold}
      ->The average user rating is nearing or has fallen below the desired threshold of [rating_threshold] stars. This suggests potential quality or usability concerns that need to be addressed.

    2. Negative Feedback Threshold:
      ->Current Negative Feedback Count: [negative_feedback_count]
      ->Threshold: {negative_feedback_threshold}
      ->The number of negative user feedback responses has approached or exceeded the threshold of {negative_feedback_threshold}. This indicates that users are experiencing significant problems with the system.
    These thresholds are in place to help us proactively identify and resolve issues before they escalate and impact a larger portion of our user base. We'd appreciate if the engineering team could prioritize the following actions:

    1. Analyze the specific negative feedback to uncover common themes, root causes, and potential solutions.
    2. Reach out to a sample of users who provided negative feedback to gather more contextual information about their experiences.
    3. Collaborate with the product and design teams to develop and implement fixes or improvements that address the user pain points.
    4. Provide progress updates to the wider organization and affected users to maintain transparency and build trust.
    5. Please review the user feedback data and submit an action plan within the next 24 hours. Let me know if you need any additional information or have any questions.

    Thank you for your prompt attention to this matter. Together, we can ensure a positive user experience and maintain the overall health of the system.

    Best regards,
    The User Feedback Monitoring System


    """

    alert_sender = NotificationSender(sender, email_addresses, password, subject, body, path)
    alert_sender.send_email()








