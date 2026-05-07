# ================================================================
# Project:     Self-Hosted SIEM System - Run (Main)
# Description: It imports all three runners and calls their 
#              main() functions in sequence with a formatted 
#              header and footer around the output. 
#
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Import All Alerts ---
import critical_alerts
import high_alerts
import all_alerts
from datetime import datetime

def main():
    print("\n" + "=" * 60)
    print("   🛡️  HUNTER'S SIEM — FULL REPORT SUITE")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\n[1/3] Running Critical Alerts...")
    critical_alerts.main()

    print("\n[2/3] Running High Severity Alerts...")
    high_alerts.main()

    print("\n[3/3] Running Full Alert Report...")
    all_alerts.main()

    print("\n" + "=" * 60)
    print("   ✅ All reports complete")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()