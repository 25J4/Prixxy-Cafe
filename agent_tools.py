import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def log_sale(menu: str, quantity: int, price: float) -> str:
    """บันทึกออเดอร์ลง Google Sheets และแจ้งเตือนผ่าน Telegram"""
    total = quantity * price
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #แจ้งเตือนผ่าน Telegram
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    tg_status = "รอกำเนินการ"
    if token and chat_id:
        message = (
            f"🔔 **ออเดอร์ใหม่!**\n"
            f"☕ เมนู: {menu}\n"
            f"🔢 จำนวน: {quantity} แก้ว\n"
            f"💰 ยอดรวม: {total} บาท\n"
            f"📅 เวลา: {timestamp}"
        )
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
            requests.post(url, json=payload)
            tg_status = "ส่งสำเร็จ ✅"
        except:
            tg_status = "ส่งไม่สำเร็จ ❌"

    #บันทึกลง Google Sheets
    sheet_status = "รอกำเนินการ"
    try:
        # ดึงข้อมูล JSON จาก Secret มาทำเป็นกุญแจเข้า Sheets
        service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(creds)
        
        # เปิดไฟล์ Sheet และบันทึกข้อมูลต่อท้าย (Append)
        sheet = client.open_by_key(sheet_id).get_worksheet(0)
        sheet.append_row([timestamp, menu, quantity, price, total])
        sheet_status = "บันทึกสำเร็จ ✅"
    except Exception as e:
        sheet_status = f"ผิดพลาด: {str(e)} ❌"

    return f"รับออเดอร์ '{menu}' {quantity} แก้ว เรียบร้อยครับ! (Telegram: {tg_status}, Sheets: {sheet_status})"

TOOLS = {
    "log_sale": log_sale,
}