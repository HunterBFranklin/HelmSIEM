# =============================================================================
# HelmSIEM — daily_recap.py
# Maintainer : github.com/HunterBFranklin/HelmSIEM
# License    : MIT
# Created    : May 06, 2026
# Modified   : June 21, 2026
# Version    : 3.0
# =============================================================================

# ----------------------------------------------------------------
# VS Code Folding Key Reference
# ----------------------------------------------------------------
# Fold all regions        →  Command + K, Command + 0
# Expand all regions      →  Command + K, Command + J
# Fold current region     →  Command + K, Command + [
# Expand current region   →  Command + K, Command + ]
# Fold all comments       →  Command + K, Command + 8
# ----------------------------------------------------------------

# region --- Imports (expand for description) ---
# Description:
# requests is imported for the ConnectionError catch.
# datetime stamps the recap subject line with today's date.
# log_event writes to alert.log so every recap run is recorded,
# including failures, useful for diagnosing why a recap didn't
# arrive on a given morning.
# endregion

import requests
from datetime import datetime
from config import (
    ES_HOST,
    SIEM_NAME,
)
from elasticsearch_client import get_recent_alerts
from recap_formatter      import format_recap
from email_reporter       import send_email_report
from utility              import log_event

# region --- Constants (expand for description) ---
# Description:
# RECAP_LOOKBACK_MINUTES is fixed at 1440 (24 hours exactly) and is
#       not pulled from .env intentionally. The daily recap is designed to
#       cover a full day.
# RECAP_SIZE=1000 is a generous ceiling that captures all but the
#       most exceptionally active days (can be increased if needed).
# endregion

RECAP_LOOKBACK_MINUTES = 1440   # 24 hours, fixed by design
RECAP_SIZE             = 1000   # max alerts per recap query
RECAP_SUBJECT = (
    f"📊 Daily Recap, {datetime.now().strftime('%B %d, %Y')}, {SIEM_NAME}"
)

# region --- main (expand for description) ---
# Description:
# Orchestrates the daily recap: query 24 hours of alerts, format
# them into the comprehensive recap HTML, and deliver via email.
# This is called by scheduler.py at the configured daily time, but
# can also be run manually at any time for testing or on-demand recaps.
#
# endregion

def main() -> None:
    print("\n" + "=" * 60)
    print(f"   🛡️  {SIEM_NAME}, Daily Recap")
    print(f"   {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
    print(f"   Lookback: {RECAP_LOOKBACK_MINUTES} minutes (24 hours)")
    print("=" * 60 + "\n")

    try:
        print("🔍 Querying Elasticsearch for last 24 hours...")
        results = get_recent_alerts(
            severity_override=1,
            lookback_override=RECAP_LOOKBACK_MINUTES,
            size_override=RECAP_SIZE,
        )

        hits  = results.get("hits", {}).get("hits", [])
        total = len(hits)

        if not hits:
            print("📭 No alerts found in the last 24 hours, no recap to send")
            log_event("Daily recap: no alerts found in last 24 hours", level="INFO")
            return

        print(f"✅ Found {total} alerts in the last 24 hours")

        print("📊 Building daily recap report...")
        report = format_recap(results)

        if not report:
            print("❌ Recap formatter returned no output")
            log_event("Daily recap: formatter returned None", level="ERROR")
            return

        print("✅ Recap report built successfully")

        print("📧 Sending daily recap email...")
        send_email_report(report, subject_override=RECAP_SUBJECT)

        log_event(f"Daily recap sent, {total} alerts over 24 hours", level="INFO")

        print("\n" + "=" * 60)
        print("   ✅ Daily recap complete")
        print("=" * 60 + "\n")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print(f"   Host: {ES_HOST}")
        print("   Make sure Docker and Wazuh are running")
        log_event("Daily recap failed, cannot connect to Elasticsearch", level="ERROR")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        log_event(f"Daily recap failed, {e}", level="ERROR")

# region --- Entry Point ---
# Can also be called directly by scheduler.py as a subprocess.
# endregion

if __name__ == "__main__":
    main()