# =============================================================================
# HelmSIEM — scheduler.py
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
# schedule is a lightweight Python library that handles recurring job
# scheduling with a simple, readable API.
#
# subprocess runs daily_recap.py as a child process rather than calling
# it as a function. This isolation means if the recap crashes or hangs,
# the scheduler process stays alive and will try again tomorrow.
# It also keeps the recap's stdout captured and logged cleanly.
#
# pathlib resolves the script path relative to this file so the
# subprocess call works regardless of which directory Python was
# launched from, a common source of "file not found" errors.
# endregion

import schedule
import subprocess
import time
from datetime import datetime
from pathlib import Path
from config import (
    RECAP_SCHEDULED_TIME,
    DAILY_RECAP_ENABLED,
    SCHEDULER_LOG_PATH,
    SIEM_NAME,
)

# region --- _log (expand for description) ---
# Description:
# The scheduler has its own logging function writing to scheduler.log,
# separate from alert.log which the rest of HelmSIEM uses. They're
# kept separate because mixing scheduler lifecycle messages (started,
# stopped, recap triggered) with alert events would make both files
# harder to read and grep through.
#
# Same format as log_event() in utility.py:
#       [YYYY-MM-DD HH:MM:SS] [LEVEL] message
# endregion

def _log(message: str, level: str = "INFO") -> None:
    """Write a timestamped line to both the terminal and scheduler.log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line      = f"[{timestamp}] [{level}] {message}"
    print(line)
    try:
        with open(SCHEDULER_LOG_PATH, "a") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"[{timestamp}] [WARNING] Could not write to scheduler.log: {e}")

# region --- run_daily_recap (expand for description) ---
# Description:
# Fires daily_recap.py as a subprocess and logs the result.
# endregion

def run_daily_recap() -> None:
    """Launch daily_recap.py as a subprocess and log its output and exit status."""
    if not DAILY_RECAP_ENABLED:
        _log("Daily recap is disabled (DAILY_RECAP_ENABLED=false), skipping", level="WARNING")
        return

    _log("Starting daily recap...")

    try:
        script_path = Path(__file__).parent / "daily_recap.py"
        result      = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            _log("Daily recap completed successfully")
            for line in result.stdout.strip().splitlines():
                _log(f"  {line}")
        else:
            _log(f"Daily recap failed (exit code {result.returncode})", level="ERROR")
            for line in result.stderr.strip().splitlines():
                _log(f"  {line}", level="ERROR")

    except Exception as e:
        _log(f"Unexpected error running daily recap: {e}", level="ERROR")

# region --- main (expand for description) ---
# Description:
# Registers the daily recap job and enters a polling loop.
# schedule.every().day.at() sets the time using 24-hour format —
# "20:00" means 8 PM. The time comes from config, which reads it
# from RECAP_HOUR and RECAP_MINUTE in .env.
#
# The while True / time.sleep(60) loop checks every 60 seconds
# whether any scheduled jobs are due. This is the standard pattern
# for the schedule library, it does no work unless a job is due,
# so CPU usage is negligible.
#
# KeyboardInterrupt (Control+C) is caught cleanly so the log
# shows "stopped by user" rather than a Python traceback.
#
# If DAILY_RECAP_ENABLED is false, we log and exit immediately
# rather than running an infinite loop that would never do anything.
# endregion

def main() -> None:
    if not DAILY_RECAP_ENABLED:
        _log(
            "Daily recap is DISABLED, set DAILY_RECAP_ENABLED=true in .env to enable",
            level="WARNING",
        )
        _log("Scheduler exiting")
        return

    _log(f"{SIEM_NAME} scheduler started, daily recap scheduled at {RECAP_SCHEDULED_TIME}")
    _log(f"Log file: {SCHEDULER_LOG_PATH}")
    _log("Press Control + C to stop")

    schedule.every().day.at(RECAP_SCHEDULED_TIME).do(run_daily_recap)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # poll every 60 seconds
    except KeyboardInterrupt:
        _log("Scheduler stopped by user")

# region --- Entry Point ---
# Run with: python3 scheduler.py
# Keep it running in a terminal, tmux session, or background process.
# endregion

if __name__ == "__main__":
    main()