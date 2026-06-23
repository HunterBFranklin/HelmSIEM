# =============================================================================
# HelmSIEM — all_alerts.py
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
# Same import pattern as the other tier runners. LOOKBACK_MINUTES
# from config controls the window for this report, the "all alerts"
# tier uses the standard lookback since it's meant for frequent
# manual review, not urgent incident response.
# endregion

import requests
from config import (
    ES_HOST,
    LOOKBACK_MINUTES,
    SIEM_NAME,
)
from elasticsearch_client import get_recent_alerts
from formatter            import format_alerts
from email_reporter       import send_email_report
from utility              import print_report

# region --- main (expand for description) ---
# Description:
# Runs the All Alerts tier: every Wazuh event at rule level 1 and
# above over the standard LOOKBACK_MINUTES window (default 15 min).
#
# size_override=50 keeps the email manageable for a 15-minute window.
# If you extend LOOKBACK_MINUTES significantly, consider raising this.
# endregion

def main() -> None:
    print(f"\n🟢 Running All Alerts Report...")
    print(f"   SIEM     : {SIEM_NAME}")
    print(f"   Host     : {ES_HOST}")
    print(f"   Levels   : 1+ (All)")
    print(f"   Window   : Last {LOOKBACK_MINUTES} minutes\n")

    try:
        results = get_recent_alerts(
            severity_override=1,
            lookback_override=LOOKBACK_MINUTES,
            size_override=50,
        )
        report = format_alerts(results, severity_label="All Alerts", severity_min=1)
        print_report(report, severity_label="All Alerts", severity_min=1)

        if report:
            send_email_report(report, subject_override=f"📋 Full Report, {SIEM_NAME} Security Alerts")
        else:
            print("📭 No alerts to report")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print("   Make sure Docker and Wazuh are running\n")

    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")

# region --- Entry Point ---
# See critical_alerts.py for a full explanation of this pattern.
# endregion

if __name__ == "__main__":
    main()