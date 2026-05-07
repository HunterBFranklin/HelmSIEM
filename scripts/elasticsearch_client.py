# ================================================================
# Project:     Self-Hosted SIEM System - Elasticsearch Client
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 06, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Search Client Function ---
import requests # HTTP calls to Elasticsearch API.
import json
from datetime import datetime # Time-based queries.
import urllib3 # SSL connection, disable certain connections.
from config import (
    ELASTICSEARCH_URL,
    ES_USER,
    ES_PASSWORD
)

# Disable SSL warnings (for self-signed certificate).
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_recent_alerts(severity_override=None, severity_max=None):

    """
    Query Elasticsearch for recent high severity alerts (rule.level 7-15).
    Returns raw results from the API.
    """
    from config import LOOKBACK_MINUTES
    
    threshold = severity_override if severity_override is not None else 1

    # Build level range filter
    level_filter = {"gte": threshold}
    if severity_max is not None:
        level_filter["lte"] = severity_max

    # Elasticsearch DSL query structure:
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": f"now-{LOOKBACK_MINUTES}m" # Range of current time to lookback time (15 mins prior).
                            }
                        }
                    },
                    {
                        "range": {
                            "rule.level": level_filter
                        }
                    }
                ]
            }
        },
        "sort": [{"@timestamp": {"order": "desc"}}], # Sorts results to newest first.
        "size": 20 # Max results of 20.
    }

    # 
    response = requests.post(
        f"{ELASTICSEARCH_URL}/wazuh-alerts-*/_search",
        auth=(ES_USER, ES_PASSWORD),
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
        verify=False # Skips SSL certificate verification.
    )

    return response.json()