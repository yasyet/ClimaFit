# CloudSheetService.py
# Author: Yasin Holzenkämpfer
# Last Modified: 15.12.2025
#
# Description: This module provides functionality to get and set the csv cloud data.
# The data is stored in a Google Sheet.

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence
import re
import csv
import io
import os

# Replace environment_variables with direct environment variable access
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")


# ----------------------------
# Configuration
# ----------------------------

DEFAULT_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DEFAULT_SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE
DEFAULT_SHEET_RANGE = "Sheet1!A1"  # where the CSV blob will be stored


# ----------------------------
# Internal helpers
# ----------------------------

def _build_sheets_service(
    service_account_file: str = DEFAULT_SERVICE_ACCOUNT_FILE,
    scopes: Sequence[str] = DEFAULT_SCOPES,
):
    from googleapiclient.discovery import build
    from google.oauth2 import service_account

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=list(scopes)
    )
    return build("sheets", "v4", credentials=creds)


def _extract_spreadsheet_id(sheet_url_or_id: str) -> str:
    # Accept either a raw spreadsheetId or a full URL.
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url_or_id)
    return m.group(1) if m else sheet_url_or_id.strip()


def _csv_to_grid(csv_text: str) -> List[List[str]]:
    if not csv_text.strip():
        return []
    buf = io.StringIO(csv_text)
    reader = csv.reader(buf)
    return [row for row in reader]


def _grid_to_csv(grid: Sequence[Sequence[str]]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    for row in grid:
        writer.writerow(list(row))
    return buf.getvalue()


# ----------------------------
# Public API
# ----------------------------

def create_new_google_sheet(sheet_name: str) -> str:
    """
    Creates a new Google Sheet with the specified name.

    Args:
        sheet_name (str): The name of the new Google Sheet.

    Returns:
        str: The URL of the newly created Google Sheet.
    """
    service = _build_sheets_service()

    spreadsheet = {"properties": {"title": sheet_name}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
    spreadsheet_id = spreadsheet.get("spreadsheetId")
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"


def google_sheet_exists(
        spreadsheet_url_or_id: str,
        service_account_file: str = DEFAULT_SERVICE_ACCOUNT_FILE
) -> bool:
    """
    Checks if a Google Sheet exists.

    Args:
        spreadsheet_url_or_id: Spreadsheet URL or spreadsheetId.
        service_account_file: Path to Google service account json.

    Returns:
        bool: True if the Google Sheet exists, False otherwise.
    """
    spreadsheet_id = _extract_spreadsheet_id(spreadsheet_url_or_id)
    service = _build_sheets_service(service_account_file=service_account_file)

    try:
        service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        return True
    except Exception:
        return False
    

def find_sheet_id_by_name(sheet_title: str, service_account_file: str = DEFAULT_SERVICE_ACCOUNT_FILE) -> Optional[int]:
    """
    Finds the sheet ID of a sheet by its title.

    Args:
        sheet_title: The title of the sheet to find.
        service_account_file: Path to Google service account json.

    Returns:
        The sheet ID if found, otherwise None.
    """
    service = _build_sheets_service(service_account_file=service_account_file)
    spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_title).execute()
    sheets = spreadsheet.get("sheets", [])
    
    for sheet in sheets:
        properties = sheet.get("properties", {})
        if properties.get("title") == sheet_title:
            return properties.get("sheetId")
    
    return None


def set_csv_data(
    spreadsheet_url_or_id: str,
    csv_text: str,
    cell_range: str = DEFAULT_SHEET_RANGE,
    service_account_file: str = DEFAULT_SERVICE_ACCOUNT_FILE,
) -> None:
    """
    Writes CSV text into the sheet starting at `cell_range` as a table (rows/columns).

    Args:
        spreadsheet_url_or_id: Spreadsheet URL or spreadsheetId.
        csv_text: CSV content to write.
        cell_range: A1 range indicating the top-left cell to write into.
        service_account_file: Path to Google service account json.
    """
    spreadsheet_id = _extract_spreadsheet_id(spreadsheet_url_or_id)
    service = _build_sheets_service(service_account_file=service_account_file)

    values = _csv_to_grid(csv_text)
    body = {"values": values}

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=cell_range,
        valueInputOption="RAW",
        body=body,
    ).execute()


def get_csv_data(
    spreadsheet_url_or_id: str,
    cell_range: str = "Sheet1!A:Z",
    service_account_file: str = DEFAULT_SERVICE_ACCOUNT_FILE,
) -> str:
    """
    Reads a rectangular range from the sheet and returns it as CSV.

    Args:
        spreadsheet_url_or_id: Spreadsheet URL or spreadsheetId.
        cell_range: A1 range to read (default reads columns A..Z).
        service_account_file: Path to Google service account json.

    Returns:
        CSV-formatted string.
    """
    spreadsheet_id = _extract_spreadsheet_id(spreadsheet_url_or_id)
    service = _build_sheets_service(service_account_file=service_account_file)

    resp = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=cell_range,
        majorDimension="ROWS",
    ).execute()

    values = resp.get("values", [])
    return _grid_to_csv(values)


def append_csv_rows(
    spreadsheet_url_or_id: str,
    csv_text: str,
    sheet_range: str = "Sheet1!A1",
    service_account_file: str = DEFAULT_SERVICE_ACCOUNT_FILE,
) -> None:
    """
    Appends CSV rows to a sheet (as rows/columns, not as a single blob).

    Args:
        spreadsheet_url_or_id: Spreadsheet URL or spreadsheetId.
        csv_text: CSV rows to append.
        sheet_range: Any range within the target sheet (used to identify the sheet).
        service_account_file: Path to Google service account json.
    """
    spreadsheet_id = _extract_spreadsheet_id(spreadsheet_url_or_id)
    service = _build_sheets_service(service_account_file=service_account_file)

    values = _csv_to_grid(csv_text)
    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()