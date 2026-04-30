import os
from pathlib import Path
from typing import List, Dict

import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


FIELDNAMES = [
    "timestamp",
    "dealer",
    "listing_url",
    "product_name",
    "product_name_clean",
    "year",
    "weight",
    "coin_family",
    "product_url",
    "price",
    "currency",
    "availability",
    "raw_price_text",
    "scrape_status",
    "error_message",
]


def get_gspread_client():
    credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

    if not credentials_path:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS_PATH is not set in .env")

    full_credentials_path = PROJECT_ROOT / credentials_path

    creds = Credentials.from_service_account_file(
        full_credentials_path,
        scopes=SCOPES,
    )

    return gspread.authorize(creds)


def get_spreadsheet():
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

    if not spreadsheet_id:
        raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID is not set in .env")

    client = get_gspread_client()
    return client.open_by_key(spreadsheet_id)


def records_to_rows(records: List[Dict]) -> List[List]:
    rows = []

    for record in records:
        row = [record.get(field) for field in FIELDNAMES]
        rows.append(row)

    return rows


def write_latest_prices(records: List[Dict]) -> None:
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("latest_prices")

    worksheet.clear()
    worksheet.append_row(FIELDNAMES)

    if records:
        worksheet.append_rows(records_to_rows(records))


def append_price_history(records: List[Dict]) -> None:
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet("price_history")

    existing_values = worksheet.get_all_values()

    if not existing_values:
        worksheet.append_row(FIELDNAMES)

    if records:
        worksheet.append_rows(records_to_rows(records))