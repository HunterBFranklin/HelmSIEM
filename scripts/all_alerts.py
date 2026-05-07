# ================================================================
# Project:     Self-Hosted SIEM System - All Alerts (1+)
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

import requests
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
    Main execution for all alerts report.
    """

    print(f"\n🟢 Running All Alerts Report...")
    print(f"     URL:       {ELASTICSEARCH_URL}")
    print(f"     Threshold: Level 1+ (All Alerts)")
    print(f"     Window:    Last {LOOKBACK_MINUTES} minutes\n")

    try:
        results = get_recent_alerts(severity_override=1)
        report = format_alerts(results, severity_label="All Alerts", severity_min=1)
        print_report(report, severity_label="All Alerts", severity_min=1)

        if report:
            send_email_report(report, subject_override="📋 Full — Wazuh Security Alert Report")
        else:
            print("📭 No alerts to report")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print(f"   Make sure Docker and Wazuh are running\n")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}\n")

if __name__ == "__main__":
    main()