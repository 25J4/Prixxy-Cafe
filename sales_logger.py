import os
import gspread
import requests
from dotenv import load_dotenv
from datetime import datetime # เครื่องมือสำหรับดูดวันที่และเวลาปัจจุบัน

#โหลดการตั้งค่า
load_dotenv()
SHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

#ยืนยันตัวตนและเปิดตาราง
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.sheet1

#เพิ่มฟังก์ชันแจ้งเตือน ผ่าน Telegram
def send_telegram_alert(menu_name, quantity, total_price):
    try:
        message = (
            f"🔔 *มีออเดอร์ใหม่เข้าค้าบผม!*\n"
            f"--------------------------\n"
            f"☕ เมนู: *{menu_name}*\n"
            f"🔥 จำนวน: {quantity} ชิ้น\n"
            f"💸 รวมเงิน: *{total_price:,.2f}* บาท\n"
            f"--------------------------\n"
            f"✅ บันทึกข้อมูลลง Google Sheets เรียบร้อย"
        )
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, data=payload)
        print("📱 ส่งแจ้งเตือนเข้า Telegram เรียบร้อย!")
    except Exception as e:
        print(f"❌ ส่งแจ้งเตือนพลาด: {e}")

#สร้างฟังก์ชันสำหรับจดยอดขาย
def log_sale(menu_name, quantity, price):
    try:
        # หาวันที่และเวลาปัจจุบัน (ตัวอย่าง: 2026-05-12 15:30:00)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # คำนวณยอดรวม (จำนวน x ราคา)
        total_price = quantity * price
        
        # จัดเรียงข้อมูลให้ตรงกับ 5 คอลัมน์ (วันที่, เมนู, จำนวน, ราคา, ยอดรวม)
        row_data = [current_time, menu_name, quantity, price, total_price]
        
        # สั่งบอทเขียนข้อมูลลงในแถวถัดไปที่ว่างอยู่
        worksheet.append_row(row_data)
        
        print(f"✅ จดยอดขายสำเร็จแล้วค้าบผม: {menu_name} | จำนวน: {quantity} | รวม: {total_price} บาท")

        # แจ้งเตือนผ่าน Telegram
        send_telegram_alert(menu_name, quantity, total_price)
        
    except Exception as e:
        print(f"❌ บอททำงานพลาด: {e}")

if __name__ == "__main__":
    print("กำลังจดยอดขายที่ตารางค้าบ...รอแป๊บ!")
    
    # ลองจำลองการขาย 2 รายการ
    log_sale("คาปูชิโน่เย็น", 2, 60)
    log_sale("ครัวซองต์เนยสด", 1, 45)