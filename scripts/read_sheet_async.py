#!/usr/bin/env python3
"""Async reader for Google Sheets using a service account and gspread_asyncio.

Usage:
  export GOOGLE_CREDS=/path/to/credentials.json  # optional, defaults to ./credentials.json
  python scripts/read_sheet_async.py --sheet-id YOUR_SHEET_ID [--worksheet 0]

Install required packages in your venv:
  pip install gspread gspread_asyncio google-auth
"""
import os
import json
import asyncio
import argparse
from typing import Union

from gspread_asyncio import AsyncioGspreadClientManager
from google.oauth2.service_account import Credentials

# Default timeout (seconds) for network operations; configurable via env GSPREAD_TIMEOUT
TIMEOUT = int(os.getenv("GSPREAD_TIMEOUT", "15"))

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_creds():
    """Return google Credentials object built from service account JSON file.
    gspread_asyncio expects a callable that returns a google-auth Credentials object.
    """
    creds_path = os.getenv("GOOGLE_CREDS", os.path.join(os.getcwd(), "credentials.json"))
    with open(creds_path, "r") as fh:
        info = json.load(fh)
    return Credentials.from_service_account_info(info, scopes=SCOPES)


async def read_sheet(spreadsheet_id: str, worksheet: Union[int, str] = 0):
    """Read all records from the given spreadsheet and worksheet.

    Returns a list of dictionaries (rows) similar to gspread's get_all_records().
    Uses timeouts to avoid indefinite hangs.
    """
    agm = AsyncioGspreadClientManager(get_creds)
    try:
        client = await asyncio.wait_for(agm.authorize(), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        raise RuntimeError(f"Authorization timed out after {TIMEOUT}s")
    except Exception as e:
        raise RuntimeError(f"Authorization failed: {e}")

    # open by id
    try:
        sh = await asyncio.wait_for(client.open_by_key(spreadsheet_id), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        raise RuntimeError(f"Opening spreadsheet timed out after {TIMEOUT}s")
    except Exception as e:
        raise RuntimeError(f"Failed to open spreadsheet '{spreadsheet_id}': {e}")

    # select worksheet by index (int) or name (str)
    try:
        if isinstance(worksheet, int):
            ws = await asyncio.wait_for(sh.get_worksheet(worksheet), timeout=TIMEOUT)
        else:
            ws = await asyncio.wait_for(sh.worksheet(worksheet), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        raise RuntimeError(f"Fetching worksheet timed out after {TIMEOUT}s")
    except Exception as e:
        raise RuntimeError(f"Failed to get worksheet '{worksheet}': {e}")

    if ws is None:
        raise RuntimeError("Worksheet not found")

    try:
        records = await asyncio.wait_for(ws.get_all_records(), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        raise RuntimeError(f"Retrieving worksheet data timed out after {TIMEOUT}s")
    except Exception as e:
        raise RuntimeError(f"Failed to read worksheet data: {e}")

    return records


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet-id", required=True, help="Google Spreadsheet ID (from the URL)")
    parser.add_argument("--worksheet", default=0, help="Worksheet index (0) or title",)
    args = parser.parse_args()

    # cast worksheet param to int when possible
    try:
        ws = int(args.worksheet)
    except Exception:
        ws = args.worksheet

    rows = await read_sheet(args.sheet_id, ws)
    print(json.dumps(rows, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
