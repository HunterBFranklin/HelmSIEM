# =============================================================================
# HelmSIEM — high_alerts.py
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
# Same import pattern as critical_alerts.py.
# endregion

import requests
from config import (
    ES_HOST,
    LOOKBACK_MINUTES,
    LEVEL_HIGH_MIN,
    LEVEL_HIGH_MAX,
    SIEM_NAME,
)
from elasticsearch_client import get_recent_alerts
from formatter            import format_alerts
from email_reporter       import send_email_report
from utility              import print_report

# region --- main (expand for description) ---
# Description:
# Runs the High severity alert tier: Wazuh rule levels 7-11 over
# the last 60 minutes. High alerts cover suspicious activity that
# doesn't yet confirm an active threat, repeated authentication
# failures, unusual process behavior, policy violations.
#
# size_override=100 is intentionally larger than Critical's 50 —
# high-severity events are more frequent, and cutting off at 50
# would miss real activity during busy periods.
# endregion

def main() -> None:
    print(f"\n🟡 Running High Severity Alerts Report...")
    print(f"   SIEM     : {SIEM_NAME}")
    print(f"   Host     : {ES_HOST}")
    print(f"   Levels   : {LEVEL_HIGH_MIN}-{LEVEL_HIGH_MAX} (High)")
    print(f"   Window   : Last 60 minutes\n")

    try:
        results = get_recent_alerts(
            severity_override=LEVEL_HIGH_MIN,
            severity_max=LEVEL_HIGH_MAX,
            lookback_override=60,
            size_override=100,
        )
        report = format_alerts(
            results,
            severity_label="High",
            severity_min=LEVEL_HIGH_MIN,
            severity_max=LEVEL_HIGH_MAX,
        )
        print_report(report, severity_label="High",
                     severity_min=LEVEL_HIGH_MIN, severity_max=LEVEL_HIGH_MAX)

        if report:
            send_email_report(report, subject_override=f"⚠️ High Severity, {SIEM_NAME} Security Alert")
        else:
            print("📭 No high severity alerts to report")

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