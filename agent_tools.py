import os
import json
import requests
import gspread
import base64
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv

def log_sale(menu: str, quantity: int, price: float) -> str:
    """บันทึกออเดอร์ลง Google Sheets และแจ้งเตือนผ่าน Telegram"""
    total = quantity * price
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    load_dotenv(override=True)
    
    # --- ส่วนที่ 1: แจ้งเตือนผ่าน Telegram ---
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    tg_status = "รอกำเนินการ"
    if token and chat_id:
        try:
            message = (
                f"🔔 *มีออเดอร์ใหม่เข้าค้าบผม!*\n"
                f"--------------------------\n"
                f"🥞 เมนู: *{menu}*\n"
                f"🔥 จำนวน: {quantity} ชิ้น\n"
                f"💸 รวมเงิน: *{total:,.2f}* บาท\n"
                f"--------------------------\n"
                f"✅ บันทึกข้อมูลลง Google Sheets เรียบร้อย"
            )
            
            url = f"https://api.telegram.org/bot{token.strip()}/sendMessage"
            payload = {
                "chat_id": chat_id.strip(),
                "text": message,
                "parse_mode": "Markdown"
            }
            requests.post(url, data=payload)
            tg_status = "ส่งสำเร็จ ✅"
        except Exception as e:
            tg_status = f"ส่งไม่สำเร็จ ❌ ({str(e)})"
    else:
        tg_status = "หารหัส Token ไม่เจอ ❌"

    # --- ส่วนที่ 2: บันทึกลง Google Sheets ---
    sheet_status = "รอกำเนินการ"
    try:
        # ดึงตัวแปร B64 จาก .env 
        b64_data = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON_B64")
        sheet_id = os.getenv("GOOGLE_SHEETS_ID")
        
        if not b64_data or not sheet_id:
            sheet_status = "หารหัสใน .env ไม่เจอ ❌"
        else:
            # ถอดรหัส Base64 กลับเป็น JSON 
            decoded_str = base64.b64decode(b64_data.strip()).decode("utf-8")
            service_info = json.loads(decoded_str)
            
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(service_info, scopes=scopes)
            client = gspread.authorize(creds)
            
            sheet = client.open_by_key(sheet_id.strip()).get_worksheet(0)
            sheet.append_row([timestamp, menu, quantity, price, total])
            sheet_status = "บันทึกสำเร็จ ✅"
            
    except Exception as e:
        sheet_status = f"ผิดพลาด: {str(e)} ❌"

    return f"รับออเดอร์ '{menu}' {quantity} ชิ้น เรียบร้อยครับ! (Telegram: {tg_status}, Sheets: {sheet_status})"

TOOLS = {
    "log_sale": log_sale,
}