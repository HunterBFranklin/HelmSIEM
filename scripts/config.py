# =============================================================================
# HelmSIEM — config.py
# Maintainer : github.com/HunterBFranklin/HelmSIEM
# License    : MIT
# Created    : May 06, 2026
# Modified   : June 21, 2026
# Version    : 3.1
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
# os + dotenv pull values out of the .env file at the repo root and
#       make them available as environment variables for this process.
# pathlib gives us clean, cross-platform file path handling, no
#       string concatenation, no OS-specific separators to worry about.
# sys is used by _require() to exit immediately with a clear message
#       if a required credential is missing.
# endregion

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# region --- Load .env (expand for description) ---
# Description:
# This block finds the .env file by walking up two directory levels
# from config.py (scripts/ → repo root) and loads it into the
# environment before any other module reads from os.getenv().
# endregion

_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

# region --- Internal Helpers (expand for description) ---
# Description:
# _require() and _optional() are private helpers that keep the rest of this file
#       clean and readable.
#
# _require() is used for values HelmSIEM absolutely cannot run
#       without, credentials, email addresses, API keys.
#
# _optional() is used for values that have sensible defaults, so
#       the system works on a fresh clone even before the user has
#       customized their .env.
# endregion

def _require(key: str) -> str:
    """Pull a required env var. Exit loudly if it's not set."""
    value = os.getenv(key, "").strip()
    if not value:
        print(f"\n[HelmSIEM] FATAL: Required env variable '{key}' is missing or empty.")
        print(f"           Add it to your .env file at: {_REPO_ROOT / '.env'}\n")
        sys.exit(1)
    return value

def _optional(key: str, default: str = "") -> str:
    """Pull an optional env var. Return default if it's not set."""
    return os.getenv(key, default).strip() or default

# region --- Project Identity (expand for description) ---
# Description:
# Human-readable labels that appear in log output, email subject
# lines, and HTML report headers. All three are pulled from .env
# so you can brand HelmSIEM for your environment without touching
# any source code. The defaults are neutral and work out of the box.
#
#       SIEM_NAME: appears in email subjects and report headers
#       OWNER_NAME: shown in report footers and log attribution
#       OWNER_GITHUB: linked in report footers; set to your GitHub URL
#
# If you leave these unset in .env, HelmSIEM uses the defaults
# below. They will appear throughout the generated emails and logs.
# endregion

SIEM_NAME    = _optional("SIEM_NAME",    "HelmSIEM")
OWNER_NAME   = _optional("OWNER_NAME",   "HelmSIEM")
OWNER_GITHUB = _optional("OWNER_GITHUB", "github.com/HunterBFranklin/HelmSIEM")

# region --- Elasticsearch (expand for description) ---
# Description:
# Elasticsearch is the database that stores every security event
# Wazuh collects. HelmSIEM queries it directly via REST API to
# pull alerts for reporting and notification dispatch.
#
# ES_HOST:         the URL of your Elasticsearch node. Defaults to
#                  localhost:9200, which is where Wazuh's Docker
#                  stack exposes it.
# 
# ES_USER /
# ES_PASSWORD:     required credentials. Wazuh sets these during
#                  stack setup; defaults are admin / SecretPassword.
# 
# ES_INDEX:        the index pattern Wazuh writes alerts into.
#                  The wildcard (*) matches all date-suffixed indexes
#                  so you always query across the full history.
# 
# ES_VERIFY_SSL:   set to false because Wazuh ships with a self-signed
#                  TLS certificate. If you're running a production deployment 
#                  with a real cert, set this to true.
# 
# ES_MAX_RESULTS:  hard cap on documents returned per query.
# endregion

ES_HOST        = _optional("ES_HOST",       "https://localhost:9200")
ES_USER        = _require("ES_USER")
ES_PASSWORD    = _require("ES_PASSWORD")
ES_INDEX       = _optional("ES_INDEX",      "wazuh-alerts-*")
ES_VERIFY_SSL  = _optional("ES_VERIFY_SSL", "false").lower() == "true"
ES_MAX_RESULTS = int(_optional("ES_MAX_RESULTS", "500"))

# Backward-compat alias, elasticsearch_client.py references ELASTICSEARCH_URL.
ELASTICSEARCH_URL = ES_HOST

# region --- Alert Severity Thresholds (expand for description) ---
# Description:
# Wazuh scores every security event on a 1-15 integer scale called
# the rule level. Higher numbers mean more severe. HelmSIEM groups
# these into three reporting tiers:
#
#   Critical  (default 12-15), active threats, exploitation attempts,
#             privilege escalation. These warrant immediate attention.
#   
#   High      (default  7-11), suspicious activity, repeated failures,
#             policy violations. Worth reviewing within the hour.
#   
#   All       (default   1+ ), everything Wazuh detected, including
#             informational and low-severity events.
#
# You can raise or lower these thresholds in .env if your environment
# generates too much noise at a given tier. No source code changes needed.
# endregion

LEVEL_CRITICAL_MIN = int(_optional("LEVEL_CRITICAL_MIN", "12"))
LEVEL_CRITICAL_MAX = int(_optional("LEVEL_CRITICAL_MAX", "15"))

LEVEL_HIGH_MIN     = int(_optional("LEVEL_HIGH_MIN",     "7"))
LEVEL_HIGH_MAX     = int(_optional("LEVEL_HIGH_MAX",     "11"))

LEVEL_ALL_MIN      = int(_optional("LEVEL_ALL_MIN",      "1"))

# region --- Live Alert Window (expand for description) ---
# Description:
# LOOKBACK_MINUTES controls how far back the three live alert runners
# (critical, high, all) look when they query Elasticsearch. This is
# separate from the daily recap, which always covers exactly 24 hours,
# and separate from the dispatcher, which tracks its own seen-alert
# state rather than relying on a fixed time window.
#
# 15 minutes is the recommended default for manual runs. If you're
# scheduling runs via cron, set this to match your cron interval.
#
# DEFAULT_SIZE is the maximum number of alert documents fetched per
# query. Each tier runner can override this independently.
# endregion

LOOKBACK_MINUTES = int(_optional("LOOKBACK_MINUTES", "15"))
DEFAULT_SIZE     = int(_optional("DEFAULT_SIZE",     "50"))

# region --- Email (Gmail SMTP) (expand for description) ---
# Description:
# HelmSIEM delivers all reports and alerts via email using Gmail's
# SMTP server with TLS encryption. To use this you need a Gmail App
# Password, a 16-character token that gives HelmSIEM permission to
# send email on your behalf without exposing your real password.
#
# How to generate a Gmail App Password:
#   1. Go to myaccount.google.com
#   2. Security → 2-Step Verification (must be enabled first)
#   3. App passwords → create one named "HelmSIEM"
#   4. Paste the 16-character result into EMAIL_PASSWORD in your .env
#
# SMTP_SERVER / SMTP_PORT, Gmail's outbound mail server settings.
#       Port 587 is the standard for authenticated, encrypted email (STARTTLS).
#       Only change these if you're using a different email provider.
#
# EMAIL_SENDER: the Gmail address sending the reports.
# EMAIL_PASSWORD: the App Password (not your Gmail login password).
# EMAIL_RECEIVER: where reports are delivered. Supports a
#       comma-separated list: user@example.com, other@example.com
# EMAIL_SUBJECT: default subject line; each alert tier overrides
#       this with a specific subject when it sends.
# endregion

SMTP_SERVER   = _optional("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT     = int(_optional("SMTP_PORT", "587"))

EMAIL_SENDER   = _require("EMAIL_SENDER")
EMAIL_PASSWORD = _require("EMAIL_PASSWORD")
EMAIL_SUBJECT  = _optional("EMAIL_SUBJECT", f"🚨 {SIEM_NAME} Alert Report")

# Parse the recipient list, support both single address and comma-separated.
_raw_receiver  = _require("EMAIL_RECEIVER")
EMAIL_RECEIVER = _raw_receiver  # kept as plain string for email_reporter.py
SMTP_TO: list[str] = [addr.strip() for addr in _raw_receiver.split(",") if addr.strip()]

# region --- Twilio SMS (expand for description) ---
# Description:
# HelmSIEM can send SMS alerts via Twilio for high-urgency events
# so you're notified immediately even when you're not checking email.
# SMS alerting is entirely optional, if TWILIO_ENABLED is false or
# any required credential is blank, SMS is silently skipped and email
# delivery is completely unaffected.
#
# How to set up Twilio (free trial is sufficient for home use):
#       1. Create a free account at twilio.com
#       2. From the Console Dashboard, copy your Account SID and Auth Token
#       3. Get a free Twilio phone number from the console
#       4. Fill in the values below, all in E.164 format: +15551234567
#
# TWILIO_ALERT_LEVEL: the minimum Wazuh rule level that triggers an SMS.
#       12 = Critical alerts only (default, recommended to avoid SMS fatigue)
#       7 = High and Critical alerts
#       1 = All alerts (very noisy; not recommended)
#
# TWILIO_COOLDOWN_CRITICAL / TWILIO_COOLDOWN_HIGH, how long (in minutes)
#       to wait before sending another SMS for the same rule ID at that
#       severity. Prevents alert storms from flooding your phone.
#       Example: if rule 5712 fires 40 times in 5 minutes, you get one SMS,
#       then silence for COOLDOWN minutes before the next one can fire.
#
# TWILIO_DIGEST_WINDOW: if multiple alerts arrive within this many
#       minutes, they are batched into a single SMS instead of one per alert.
#       Example: "3 Critical alerts; Brute Force (x2), Privilege Escalation
#       (x1). View dashboard" instead of 3 separate messages.
#       Set to 0 to disable digest mode and send one SMS per alert.
#
# TWILIO_QUIET_START / TWILIO_QUIET_END, quiet hours in 24-hour time
#       (HH:MM format). Non-critical alerts are held during this window
#       and delivered when quiet hours end. Critical alerts (level 12+)
#       always fire immediately regardless of quiet hours, a real threat
#       does not respect your sleep schedule.
#       Example: TWILIO_QUIET_START=23:00, TWILIO_QUIET_END=07:00
#       Set both to the same value to disable quiet hours entirely.
#
# TWILIO_DASHBOARD_URL: the base URL of your HelmSIEM dashboard,
#       used to generate deep links in SMS messages. Each SMS includes a
#       link directly to the specific alert that triggered it.
#       Example: https://helmsiem.vercel.app
#       Leave blank if your dashboard isn't set up yet, links are omitted.
# endregion

TWILIO_ENABLED     = _optional("TWILIO_ENABLED",     "false").lower() == "true"
TWILIO_ACCOUNT_SID = _optional("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN  = _optional("TWILIO_AUTH_TOKEN",  "")
TWILIO_FROM_NUMBER = _optional("TWILIO_FROM_NUMBER", "")
TWILIO_TO_NUMBER   = _optional("TWILIO_TO_NUMBER",   "")
TWILIO_ALERT_LEVEL = int(_optional("TWILIO_ALERT_LEVEL", "12"))

TWILIO_COOLDOWN_CRITICAL = int(_optional("TWILIO_COOLDOWN_CRITICAL", "15"))
TWILIO_COOLDOWN_HIGH     = int(_optional("TWILIO_COOLDOWN_HIGH",     "30"))

TWILIO_DIGEST_WINDOW  = int(_optional("TWILIO_DIGEST_WINDOW",  "5"))
TWILIO_QUIET_START    = _optional("TWILIO_QUIET_START", "23:00")
TWILIO_QUIET_END      = _optional("TWILIO_QUIET_END",   "07:00")
TWILIO_DASHBOARD_URL  = _optional("TWILIO_DASHBOARD_URL", "")

# region --- Notification Dispatcher (expand for description) ---
# Description:
# The dispatcher is HelmSIEM's always-on notification layer. It runs
# independently of the tier runners (run.py) on its own polling
# schedule, watches Elasticsearch for new alerts above the configured
# threshold, and routes them to the right delivery channel.
#
# DISPATCHER_ENABLED: master switch. Set to false to disable all
#       automatic notifications without stopping the scheduler or any
#       other part of HelmSIEM.
#
# DISPATCHER_POLL_INTERVAL: how often (in seconds) the dispatcher
#       checks Elasticsearch for new alerts. 60 seconds means you're
#       notified within about a minute of a real event. Lower values
#       increase responsiveness but also increase Elasticsearch query load.
#       For a homelab, 60 seconds is the right balance.
#
# DISPATCHER_LOOKBACK: how far back (in minutes) the dispatcher
#       looks on each poll. This creates a rolling window of visibility.
#       Should be slightly larger than DISPATCHER_POLL_INTERVAL to ensure
#       no alerts fall through the gap between polls. Default: 2 minutes.
#
# DISPATCHER_EMAIL_LEVEL: minimum rule level to trigger an email
#       notification via the dispatcher. This is separate from the full
#       report emails sent by run.py, this is for immediate single-alert
#       notifications. Set to 0 to disable dispatcher email entirely
#       (full reports from run.py are unaffected).
#
# DISPATCHER_SMS_LEVEL: minimum rule level to trigger an SMS.
#       Defaults to TWILIO_ALERT_LEVEL if not set separately. Allows you
#       to set different thresholds for email vs SMS independently.
#       Example: email at level 7, SMS only at level 12.
# endregion

DISPATCHER_ENABLED       = _optional("DISPATCHER_ENABLED",       "true").lower() == "true"
DISPATCHER_POLL_INTERVAL = int(_optional("DISPATCHER_POLL_INTERVAL", "60"))
DISPATCHER_LOOKBACK      = int(_optional("DISPATCHER_LOOKBACK",      "2"))
DISPATCHER_EMAIL_LEVEL   = int(_optional("DISPATCHER_EMAIL_LEVEL",   "12"))
DISPATCHER_SMS_LEVEL     = int(_optional("DISPATCHER_SMS_LEVEL",     "12"))
DISPATCHER_LOG_PATH      = None  # set below after LOGS_DIR is defined

# region --- Scheduler (expand for description) ---
# Description:
# The daily recap is a comprehensive 24-hour summary email delivered
# automatically once per day by scheduler.py.
#
# RECAP_HOUR / RECAP_MINUTE, when to send the recap, in 24-hour
#       time. Default is 20:00 (8 PM local time). Set RECAP_HOUR=7 and
#       RECAP_MINUTE=30 for 7:30 AM, for example.
#
# DAILY_RECAP_ENABLED: quick kill switch. Set to "false" in .env
#       to pause the daily recap entirely without stopping the scheduler
#       process or modifying any source code.
# endregion

RECAP_HOUR           = int(_optional("RECAP_HOUR",   "20"))
RECAP_MINUTE         = int(_optional("RECAP_MINUTE", "0"))
RECAP_SCHEDULED_TIME = f"{RECAP_HOUR:02d}:{RECAP_MINUTE:02d}"
DAILY_RECAP_ENABLED  = _optional("DAILY_RECAP_ENABLED", "true").lower() == "true"

# region --- Paths (expand for description) ---
# Description:
# Absolute filesystem paths to the repo's key directories. 
#
# LOGS_DIR.mkdir() is called at import time so the logs/ directory
#       is created automatically on first run. 
# endregion

SCRIPTS_DIR   = _REPO_ROOT / "scripts"
TEMPLATES_DIR = _REPO_ROOT / "templates"
LOGS_DIR      = _REPO_ROOT / "logs"

LOGS_DIR.mkdir(parents=True, exist_ok=True)

ALERT_LOG_PATH      = LOGS_DIR / "alert.log"
SCHEDULER_LOG_PATH  = LOGS_DIR / "scheduler.log"
DISPATCHER_LOG_PATH = LOGS_DIR / "dispatcher.log"

# region --- Wazuh Agent Map (expand for description) ---
# Description:
# This dictionary maps Wazuh's internal agent IDs (short numeric
# strings like "001") to human-readable display names that appear
# in email reports and log output.
#
# Wazuh assigns agent IDs automatically when you enroll a new
# endpoint. To find your agent IDs:
#   - Open the Wazuh dashboard → Agents
#   - Or run inside the manager container:
#       docker exec -it wazuh-manager /var/ossec/bin/agent_control -l
#
# Agents that aren't in your environment: leave the ID blank ("")
# in .env and the entry will be excluded automatically.
# Do not remove lines from this file, just leave unused ones empty.
#
# Common home network / homelab endpoints are pre-configured below.
# Add your own by following the same pattern at the bottom.
# endregion

def _agent(id_key: str, label_key: str, default_label: str):
    """Include agent in map only if an ID is configured in .env."""
    agent_id    = _optional(id_key,    "")
    agent_label = _optional(label_key, default_label)
    return (agent_id, agent_label) if agent_id else None

_agent_entries = [
    # --- Workstations & Laptops ---
    _agent("AGENT_ID_MACBOOK",    "AGENT_LABEL_MACBOOK",    "MacBook"),
    _agent("AGENT_ID_WINDOWS_PC", "AGENT_LABEL_WINDOWS_PC", "Windows PC"),
    _agent("AGENT_ID_LINUX_PC",   "AGENT_LABEL_LINUX_PC",   "Linux Workstation"),

    # --- Servers & Virtual Machines ---
    _agent("AGENT_ID_UBUNTU_VM",    "AGENT_LABEL_UBUNTU_VM",    "Ubuntu VM"),
    _agent("AGENT_ID_DEBIAN_VM",    "AGENT_LABEL_DEBIAN_VM",    "Debian VM"),
    _agent("AGENT_ID_NAS",          "AGENT_LABEL_NAS",          "NAS"),
    _agent("AGENT_ID_HOME_SERVER",  "AGENT_LABEL_HOME_SERVER",  "Home Server"),

    # --- Network Devices ---
    _agent("AGENT_ID_ROUTER",   "AGENT_LABEL_ROUTER",   "Router"),
    _agent("AGENT_ID_FIREWALL", "AGENT_LABEL_FIREWALL", "Firewall"),
    _agent("AGENT_ID_SWITCH",   "AGENT_LABEL_SWITCH",   "Network Switch"),
    _agent("AGENT_ID_AP",       "AGENT_LABEL_AP",       "Access Point"),

    # --- IoT & Other ---
    _agent("AGENT_ID_RASPBERRYPI", "AGENT_LABEL_RASPBERRYPI", "Raspberry Pi"),
    _agent("AGENT_ID_CUSTOM_1",    "AGENT_LABEL_CUSTOM_1",    "Custom Device 1"),
    _agent("AGENT_ID_CUSTOM_2",    "AGENT_LABEL_CUSTOM_2",    "Custom Device 2"),
]

AGENT_MAP: dict[str, str] = {
    agent_id: label
    for entry in _agent_entries
    if entry is not None
    for agent_id, label in [entry]
}