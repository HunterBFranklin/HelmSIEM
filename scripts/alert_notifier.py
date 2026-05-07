# =============================================================
# Project:     Personal SIEM - Alert Notifier
# Description: Queries Elasticsearch for high severity Wazuh
#              alerts and outputs a formatted security report
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 06, 2026
# Version:     1.0
# GitHub:      github.com/HunterBFranklin/ubuntu-siem
# =============================================================

# --- Imports for GH ---
from dotenv import load_dotenv
import os
load_dotenv()

# --- Imports for Report Function ---
import requests # HTTP calls to Elasticsearch API.
import json
from datetime import datetime, timedelta, timezone # Time-based queries.
import urllib3 # SSL connection, disable certain connections.

# --- Imports for Email Notification Function ---
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Disable SSL warnings (for self-signed certificate).
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Report Config ---
ELASTICSEARCH_URL   = "https://localhost:9200"
ES_USER            = os.getenv("ES_USER")
ES_PASSWORD        = os.getenv("ES_PASSWORD")
SEVERITY_THRESHOLD  = 7 # Alert on rule.level 7 or above (to 15).
LOOKBACK_MINUTES    = 15

# --- Email Config ---
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SUBJECT   = "🚨 Wazuh Security Alert Report"
SMTP_SERVER     = "smtp.gmail.com"
SMTP_PORT       = 587

def get_recent_alerts():

    """
    Query Elasticsearch for recent high severity alerts (rule.level 7-15).
    Returns raw results from the API.
    """

    # Calculation for query search window (current time - 15min lookback).
    time_from = (datetime.now(timezone.utc) - timedelta(minutes=LOOKBACK_MINUTES)).strftime('%Y-%m-%dT%H:%M:%S')

    # Elasticsearch DSL query structure:
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "timestamp": {
                                "gte": time_from # Range of current time to lookback time (15 mins prior).
                            }
                        }
                    },
                    {
                        "range": {
                            "rule.level": {
                                "gte": SEVERITY_THRESHOLD # 7 and up only.
                            }
                        }
                    }
                ]
            }
        },
        "sort": [{"timestamp": {"order": "desc"}}], # Sorts results to newest first.
        "size": 20 # Max results of 20.
    }

    # 
    response = requests.post(
        f"{ELASTICSEARCH_URL}/wazuh-alerts-*/_search",
        auth=(ES_USER, ES_PASSWORD),
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
        verify=False # Skips SSL certificate verification.
    )

    return response.json()

def format_alerts(results):

    """
    Format the raw results from get_recent_results() into a readable report.
    Returns formatted string or None (if not alerts are found).
    """

    # Extract the hits from the response.
    hits = results.get("hits", {}).get("hits", [])

    # If no alerts were present in lookback.
    if not hits:
        return None
    
    # Creates the report header.
    report  =   "=" * 60 + "\n"
    report +=   "   WAZUH SECURITY ALERT REPORT\n"
    report +=   f"  Generated: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
    report +=   f"  Alerts Found: {len(hits)}\n"
    report +=   f"  Severity Threshold: Level {SEVERITY_THRESHOLD}+\n"
    report +=   f"  Lookback Window: {LOOKBACK_MINUTES} minutes\n"
    report +=   "=" * 60 + "\n\n"

    # Loop through each alert and format.
    for hit in hits:
        source = hit.get("_source", {})
        rule   = source.get("rule", {})
        agent  = source.get("agent", {})

        # Gathers pertinent hit info (time, agent, rule level & ID, desc., and MITRE).
        report += f"⚠️  ALERT DETECTED\n"
        report += f"  Time:        {source.get('timestamp', 'Unknown')}\n"
        report += f"  Agent:       {agent.get('name', 'Unknown')}\n"
        report += f"  Rule Level:  {rule.get('level', 'Unknown')}\n"
        report += f"  Rule ID:     {rule.get('id', 'Unknown')}\n"
        report += f"  Description: {rule.get('description', 'Unknown')}\n"
        report += f"  MITRE:       {rule.get('mitre', {}).get('technique', ['None'])[0] if rule.get('mitre') else 'None'}\n"
        report += "-" * 60 + "\n\n"

    return report

def print_report(report):
    """
    Print the formatted report to terminal.
    """
    if report:
        print(report)
    else:
        print("\n" + "=" * 60)
        print(f"  NO ALERTS FOUND")
        print(f"  Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Threshold: Level {SEVERITY_THRESHOLD}+")
        print(f"  Window:    Last {LOOKBACK_MINUTES} minutes")
        print("=" * 60 + "\n")

def send_email_report(report):
    """
    Send the formatted alert report via email.
    """
    try:
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

def main():
    """
    Main execution.
    """

    # Query information printed for view in user terminal.
    print(f"\n🔍 Querying Wazuh/Elasticsearch...")
    print(f"   URL:       {ELASTICSEARCH_URL}")
    print(f"   Threshold: Level {SEVERITY_THRESHOLD}+")
    print(f"   Window:    Last {LOOKBACK_MINUTES} minutes\n")
    
    # Queries Elasticsearch, formats raw data, and prints report.
    try:
        results = get_recent_alerts()
        report = format_alerts(results)
        print_report(report)
        if report:
            send_email_report(report)
        else:
            print("📭 No alerts to email")
        
    # Exceptions to print in terminal.
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print("   Make sure Docker and Wazuh are running")
        print(f"   Expected at: {ELASTICSEARCH_URL}\n")
    
    # True exception in retrieval.
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}\n")

# --- Entry Point ---
if __name__ == "__main__":
    main()