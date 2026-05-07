# ================================================================
# Project:     Self-Hosted SIEM System - Config
# Author:      Hunter B. Franklin
# Created:     May 06, 2026
# Modified:    May 07, 2026
# Version:     1.5
# GitHub:      github.com/HunterBFranklin/selfhosted-siem-system
# ================================================================

# --- Imports for Config ---
from dotenv import load_dotenv
import os
load_dotenv()

# --- Report Config ---
ELASTICSEARCH_URL   = "https://localhost:9200"
ES_USER             = os.getenv("ES_USER")
ES_PASSWORD         = os.getenv("ES_PASSWORD")
LOOKBACK_MINUTES    = 15 # Lookback time (min).

# --- Email Config ---
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SUBJECT   = "🚨 Wazuh Security Alert Report"
SMTP_SERVER     = "smtp.gmail.com"
SMTP_PORT       = 587