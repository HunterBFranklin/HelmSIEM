# ================================================================
# Project:     Self-Hosted SIEM System - Email Report Notif.
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Email Notification Function ---
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    EMAIL_SENDER,
    EMAIL_RECEIVER,
    EMAIL_PASSWORD,
    EMAIL_SUBJECT,
    SMTP_SERVER,
    SMTP_PORT
)

def send_email_report(report, subject_override=None):
    """
    Send the formatted alert report via email.
    """

    try:
        # Determine subject.
        subject = subject_override if subject_override is not None else EMAIL_SUBJECT

        # Build the email object.
        msg = MIMEMultipart()
        msg['From']    = EMAIL_SENDER
        msg['To']      = EMAIL_RECEIVER
        msg['Subject'] = EMAIL_SUBJECT
        
        # Add the report as the email body.
        msg.attach(MIMEText(report, 'plain')) # Plain txt, not HTML.
        
        # Connect to Gmail and send report.
        print("📧 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT) # Port 587.SMTP for authenticated, encrypted email.
        server.starttls() # Encrypted TLS connection.
        server.login(EMAIL_SENDER, EMAIL_PASSWORD) # Authenticates with .env inputs.
        server.send_message(msg)
        server.quit() # Closes SMTP connection.
        
        print(f"✅ Report emailed to {EMAIL_RECEIVER}")
        
    except smtplib.SMTPAuthenticationError: # Credential error catch.
        print("❌ Email failed: Authentication error")
        print("   Check your Gmail address and app password")
        
    except smtplib.SMTPException as e: # SMTP error catch.
        print(f"❌ Email failed: {str(e)}")
        
    except Exception as e: # Catch-all.
        print(f"❌ Unexpected email error: {str(e)}")
