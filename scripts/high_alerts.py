# ================================================================
# Project:     Self-Hosted SIEM System - High Alerts (7-11)
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 06, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Main Execution ---
import requests # HTTP calls to Elasticsearch API.
from config import (
    ELASTICSEARCH_URL,
    LOOKBACK_MINUTES
)
from elasticsearch_client import get_recent_alerts
from formatter import format_alerts
from email_reporter import send_email_report
from utility import print_report

def main():
    """
    Main execution for high alerts report.
    """

    print(f"\n🟡 Running High Severity Alerts Report...")
    print(f"     URL:       {ELASTICSEARCH_URL}")
    print(f"     Threshold: Level 7-11")
    print(f"     Window:    Last {LOOKBACK_MINUTES} minutes\n")
    
    # Queries Elasticsearch, formats raw data, and prints report.
    try:
        results = get_recent_alerts(severity_override=7, severity_max=11)
        report = format_alerts(results, severity_label="High", severity_min=7, severity_max=11)
        print_report(report, severity_label="High", severity_min=7, severity_max=11)

        if report:
            send_email_report(report, subject_override="⚠️ High Severity — Wazuh Security Alert")
        else:
            print("📭 No high severity alerts to report")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print(f"   Make sure Docker and Wazuh are running\n")
    
    # True exception in retrieval.
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}\n")

# --- Entry Point ---
if __name__ == "__main__":
    main()