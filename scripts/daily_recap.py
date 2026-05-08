# ================================================================
# Project:     Self-Hosted SIEM System - Daily Recap
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     3.0
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Daily Recap ---
import requests
from datetime import datetime
from pathlib import Path
from config import ELASTICSEARCH_URL
from elasticsearch_client import get_recent_alerts
from recap_formatter import format_recap
from email_reporter import send_email_report
from utility import log_event

# Daily recap config.
RECAP_LOOKBACK_MINUTES = 1440          # 24 hours.
RECAP_SIZE             = 1000          # Max alerts to pull for period.
RECAP_SUBJECT = f"📊 Daily Recap — {datetime.now().strftime('%B %d, %Y')} — Hunter's Self-Hosted SIEM"

# Log file path.
LOG_PATH = Path(__file__).parent.parent / "logs" / "alert.log"

# Follows the same logic as other alert runners.
def main():
    """
    Main execution flow for the daily recap.
    Queries all alerts from the last 24 hours regardless of severity,
    formats them into a comprehensive recap report, and delivers via email.
    """

    print("\n" + "=" * 60)
    print("   🛡️  HUNTER'S DAILY SIEM RECAP")
    print(f"   {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
    print(f"   Lookback: {RECAP_LOOKBACK_MINUTES} minutes (24 hours)")
    print("=" * 60 + "\n")

    try:
        # Query all alerts from last 24 hours:
        print("🔍 Querying Elasticsearch for last 24 hours...")
        results = get_recent_alerts(
            severity_override=1,
            lookback_override=RECAP_LOOKBACK_MINUTES,
            size_override=RECAP_SIZE
        )

        hits = results.get("hits", {}).get("hits", [])
        total = len(hits)

        if not hits:
            print("📭 No alerts found in the last 24 hours — no recap to send")
            log_event("Daily recap: no alerts found in last 24 hours", level="INFO")
            return

        print(f"✅ Found {total} alerts in the last 24 hours")

        # Format the recap email.
        print("📊 Building daily recap report...")
        report = format_recap(results)

        if not report:
            print("❌ Recap formatter returned no output")
            log_event("Daily recap: formatter returned None", level="ERROR")
            return

        print("✅ Recap report built successfully")

        # Send the recap email.
        print("📧 Sending daily recap email...")
        send_email_report(report, subject_override=RECAP_SUBJECT)

        log_event(f"Daily recap sent — {total} alerts over 24 hours", level="INFO")

        print("\n" + "=" * 60)
        print("   ✅ Daily recap complete")
        print("=" * 60 + "\n")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print("   Make sure Docker and Wazuh are running")
        log_event("Daily recap failed — cannot connect to Elasticsearch", level="ERROR")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        log_event(f"Daily recap failed — {str(e)}", level="ERROR")


# Entry point.
if __name__ == "__main__":
    main()