import json
import os

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    """รองรับทั้งโหมดไฟล์ (local) และโหมด JSON string (GitHub Actions)"""
    json_str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    file_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

    if json_str: # โหมด Actions
        info = json.loads(json_str)
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    elif file_path: # โหมด local
        creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)
    else:
        raise RuntimeError(
            "ไม่พบ GOOGLE_SERVICE_ACCOUNT_JSON หรือ GOOGLE_SERVICE_ACCOUNT_FILE"
        )

    client = gspread.authorize(creds)
    # 🚨 ตรงนี้ในภาพเขียนว่า GOOGLE_SHEETS_ID เช็คใน .env ของคุณด้วยนะครับว่าใช้ชื่อไหน
    sheet_id = os.getenv("GOOGLE_SHEETS_ID") or os.getenv("SPREADSHEET_ID")
    return client.open_by_key(sheet_id).sheet1