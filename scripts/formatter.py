# ================================================================
# Project:     Self-Hosted SIEM System - Report Format
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Format Function ---
from datetime import datetime
from config import LOOKBACK_MINUTES
from utility import format_timestamp

def format_alerts(results, severity_label=None, severity_min=None, severity_max=None):

    """
    Format raw results from get_recent_alerts() into a readable report.
    Accepts optional severity context from the calling runner.
    Returns formatted string or None if no alerts are found.
    """

    # Extract the hits from the response.
    hits = results.get("hits", {}).get("hits", [])

    # If no alerts were present in lookback.
    if not hits:
        return None
    
    # Build severity range string for header.
    if severity_min and severity_max:
        severity_str = f"Level {severity_min}-{severity_max}"
    elif severity_min:
        severity_str = f"Level {severity_min}+"
    else:
        severity_str = "All Levels"

    label = severity_label if severity_label else severity_str
    
    # Creates the report header.
    report  =   "=" * 60 + "\n"
    report +=   "   WAZUH SECURITY ALERT REPORT\n"
    report +=   f"  Generated: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n"
    report +=   f"  Alerts Found: {len(hits)}\n"
    report +=   f"  Severity Range: {label}\n"
    report +=   f"  Lookback Window: {LOOKBACK_MINUTES} minutes\n"
    report +=   "=" * 60 + "\n\n"

    # Loop through each alert and format.
    for hit in hits:
        source = hit.get("_source", {})
        rule   = source.get("rule", {})
        agent  = source.get("agent", {})

        # Gathers pertinent hit info (time, agent, rule level & ID, desc., and MITRE).
        report += f"⚠️  ALERT DETECTED\n"
        report += f"  Time:        {source.get('timestamp', 'Unknown')}\n"
        report += f"  Agent:       {agent.get('name', 'Unknown')}\n"
        report += f"  Rule Level:  {rule.get('level', 'Unknown')}\n"
        report += f"  Rule ID:     {rule.get('id', 'Unknown')}\n"
        report += f"  Description: {rule.get('description', 'Unknown')}\n"
        report += f"  MITRE:       {rule.get('mitre', {}).get('technique', ['None'])[0] if rule.get('mitre') else 'None'}\n"
        report += "-" * 60 + "\n\n"

    return report