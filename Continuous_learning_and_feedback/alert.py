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


def send_alert(avg_rating, rating_threshold, negative_feedback_count, negative_feedback_threshold):
    # Set up email details
    sender_email = "app.technicalteam@gmail.com"

    receiver_email = "vishalkumars.work@gmail.com"
    password = os.environ.get('EMAIL_PASSWORD')
    subject = f"User Feedback Alert - System Approaching Thresholds"

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
            logging.info("E-mail alert sent successfully")
            st.success(f"Alert report email ✉️ have been sent to the {receiver_email}.")
            st.warning("📬 Haven't received the email invitation? Check your spam folder for any missed messages!")

    except Exception as e:
            logging.error(f"Error sending email: {e}")
            st.error("An error occurred while sending the email alerts. Please try again later.")


