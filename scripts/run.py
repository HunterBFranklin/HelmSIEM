# =============================================================================
# HelmSIEM — run.py
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

# region --- Overview (expand for description) ---
# Description:
# run.py is the master entry point for HelmSIEM's live alert suite.
# Running this file executes all three severity tier reports in
# sequence, Critical (12-15), High (7-11), and All (1+).
#
# Usage:
#       python3 run.py
#
# To run a single tier instead:
#       python3 critical_alerts.py
#       python3 high_alerts.py
#       python3 all_alerts.py
#
# For the daily 24-hour recap, see scheduler.py and daily_recap.py.
# endregion

# region --- Imports (expand for description) ---
# Description:
# Each tier runner is its own module with its own main() function.
# endregion

import critical_alerts  # Wazuh rule levels 12-15
import high_alerts      # Wazuh rule levels 7-11
import all_alerts       # Wazuh rule levels 1+
from datetime import datetime
from config import SIEM_NAME

# region --- main (expand for description) ---
# Description:
# Calls each tier runner in order from highest to lowest severity.
# Critical runs first so that if something urgent happened, it's
# in your inbox before the lower-tier emails arrive. Each runner
# is wrapped in the same try/except pattern internally, if one
# fails, the others still run.
# endregion

def main() -> None:
    print("\n" + "=" * 60)
    print(f"   🛡️  {SIEM_NAME}, Full Report Suite")
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

# region --- Entry Point ---
# See critical_alerts.py for a full explanation of this pattern.
# endregion

if __name__ == "__main__":
    main()