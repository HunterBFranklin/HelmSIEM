# ================================================================
# Project:     HelmSIEM — Self-Hosted Security Monitoring
# File:        run.py
#
# Description: The main entry point for HelmSIEM's alert reporting
#              suite. Running this file triggers all three severity
#              tier reports in sequence — critical, high, and full.
#              Each report queries your Elasticsearch instance,
#              formats the results, and sends an email. Run this
#              manually anytime or point a cron job at it for
#              automated reporting.
#
#              Usage: python3 run.py
#
# Maintainer:  Hunter B. Franklin
# GitHub:      github.com/HunterBFranklin/helm-siem
# License:     MIT
# Created:     May 06, 2026
# Modified:    May 10, 2026
# Version:     3.0
# ================================================================

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
# The three severity tier runners — each one is its own file
# that handles a specific range of Wazuh rule levels. We import
# them here so we can call their main() functions one after
# another. datetime stamps the header with the current time so
# every run is clearly logged in your terminal output.
# endregion

import critical_alerts  # handles rule levels 12-15.
import high_alerts      # handles rule levels 7-11.
import all_alerts       # handles rule levels 1+.
from datetime import datetime

# region --- Main Runner (expand for description) ---
# Description:
# This is the orchestrator function. It calls each severity tier
# report in order and wraps the whole run in a formatted header
# and footer so the terminal output is easy to read at a glance.
# If you only want to run one tier at a time you can call that
# file directly — e.g. python3 critical_alerts.py
# endregion

def main():
    print("\n" + "=" * 60)
    print("   🛡️  HelmSIEM — Full Report Suite")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\n[1/3] Running Critical Alerts (Level 12-15)...")
    critical_alerts.main()

    print("\n[2/3] Running High Severity Alerts (Level 7-11)...")
    high_alerts.main()

    print("\n[3/3] Running Full Alert Report (Level 1+)...")
    all_alerts.main()

    print("\n" + "=" * 60)
    print("   ✅ All reports complete")
    print("=" * 60 + "\n")

# region --- Entry Point (expand for description) ---
# Description:
# Standard Python entry point check. This makes sure main() only
# runs when you execute this file directly — not when another
# file imports it. Every executable Python script in HelmSIEM
# ends with this pattern.
# endregion

if __name__ == "__main__":
    main()