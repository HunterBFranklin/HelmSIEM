# ================================================================
# Project:     Self-Hosted SIEM System - Utility
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Print Function ---
from datetime import datetime
from config import LOOKBACK_MINUTES

def print_report(report, severity_label=None, severity_min=None, severity_max=None):
    """
    Print summary to terminal or output.
    Accepts optional severity context for clearer output.
    """

    # Build severity range string for display.
    if severity_min and severity_max:
        range_str = f"Level {severity_min}-{severity_max}"
    elif severity_min:
        range_str = f"Level {severity_min}+"
    else:
        range_str = "Level 1+"

    label = severity_label if severity_label else range_str

    if report:
        print("✅ Report generated successfully")
        print(f"   Severity:  {label}")
        print(f"   Window:    Last {LOOKBACK_MINUTES} minutes")
        print(f"   Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("\n" + "=" * 60)
        print(f"  NO ALERTS FOUND")
        print(f"  Severity:  {label}")
        print(f"  Window:    Last {LOOKBACK_MINUTES} minutes")
        print(f"  Time:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60 + "\n")


def log_event(message, level="INFO"):
    """
    Simple logger — prints timestamped messages to terminal
    and appends to alert.log
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line  = f"[{timestamp}] [{level}] {message}"

    # Print to terminal.
    print(log_line)

    # Append to log file.
    try:
        with open("../logs/alert.log", "a") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"[{timestamp}] [WARNING] Could not write to log file: {str(e)}")


def format_timestamp(raw_timestamp):
    """
    Cleans up Elasticsearch timestamp format for display.
    Converts 2026-05-07T02:11:14.513+0000 to 2026-05-07 02:11:14
    """
    try:
        return raw_timestamp[:19].replace("T", " ")
    except Exception:
        return raw_timestamp
