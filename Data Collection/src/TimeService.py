# TimeService.py
# Author: Yasin Holzenkämpfer
# Last Modified: 15.12.2025
#
# Description: This module provides functionality to get the current time.

from __future__ import annotations

import datetime

# ----------------------------
# Public API
# ----------------------------

def get_current_date() -> str:
    """Get the current date in DD-MM-YYYY format."""
    return datetime.datetime.now().strftime("%d-%m-%Y")

def get_current_time() -> str:
    """Get the current time in HH:MM:SS format."""
    return datetime.datetime.now().strftime("%H:%M:%S")