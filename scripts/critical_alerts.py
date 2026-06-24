# =============================================================================
# HelmSIEM — critical_alerts.py
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
# requests is imported here only for the ConnectionError catch.
# endregion

import requests
from config import (
    ES_HOST,
    LOOKBACK_MINUTES,
    LEVEL_CRITICAL_MIN,
    LEVEL_CRITICAL_MAX,
    SIEM_NAME,
)
from elasticsearch_client import get_recent_alerts
from formatter            import format_alerts
from email_reporter       import send_email_report
from utility              import print_report

# region --- main (expand for description) ---
# Description:
# Runs the Critical alert tier: Wazuh rule levels 12-15 over the
# last 60 minutes. Critical alerts represent active threats —
# exploitation attempts, privilege escalation, confirmed intrusions.
# endregion

def main() -> None:
    print(f"\n🔴 Running Critical Alerts Report...")
    print(f"   SIEM     : {SIEM_NAME}")
    print(f"   Host     : {ES_HOST}")
    print(f"   Levels   : {LEVEL_CRITICAL_MIN}-{LEVEL_CRITICAL_MAX} (Critical)")
    print(f"   Window   : Last 60 minutes\n")

    try:
        results = get_recent_alerts(
            severity_override=LEVEL_CRITICAL_MIN,
            severity_max=LEVEL_CRITICAL_MAX,
            lookback_override=60,
            size_override=50,
        )
        report = format_alerts(
            results,
            severity_label="Critical",
            severity_min=LEVEL_CRITICAL_MIN,
            severity_max=LEVEL_CRITICAL_MAX,
        )
        print_report(report, severity_label="Critical",
                     severity_min=LEVEL_CRITICAL_MIN, severity_max=LEVEL_CRITICAL_MAX)

        if report:
            send_email_report(report, subject_override=f"🚨 CRITICAL, {SIEM_NAME} Security Alert")
        else:
            print("📭 No critical alerts to report")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to Elasticsearch")
        print("   Make sure Docker and Wazuh are running\n")

    except Exception as e:
        print(f"❌ Unexpected error: {e}\n")

# region --- Entry Point (expand for description) ---
# Description:
# This pattern is used in every HelmSIEM script.
# endregion

if __name__ == "__main__":
    main()