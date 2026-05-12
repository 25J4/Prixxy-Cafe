import sys
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from sheets_client import get_sheet  # ดึงฟังก์ชันมาจากไฟล์ที่เราแยกไว้

# 1. โหลดการตั้งค่าจาก .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 2. ฟังก์ชันแจ้งเตือน Telegram (ยกมาจากโค้ดเดิมของคุณเป๊ะๆ)
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

# 3. ฟังก์ชันหลักสำหรับรับค่าจาก Command Line และจดยอดขาย
def log_sale():
    # ตรวจสอบรูปแบบการพิมพ์ (เช่น python sales_logger.py "ลาเต้:1:60")
    if len(sys.argv) < 2:
        print("❌ รูปแบบผิด! ต้องพิมพ์: python sales_logger.py \"เมนู:จำนวน:ราคา\"")
        return

    input_data = sys.argv[1] # รับค่า "เมนู:จำนวน:ราคา"
    
    try:
        # แยกข้อมูลและคำนวณ
        menu, qty, price = input_data.split(":")
        qty = int(qty)
        price = float(price)
        total_price = qty * price
        
        # เตรียมข้อมูลวันที่
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [current_time, menu, qty, price, total_price]

        # 4. จดลง Google Sheets ผ่าน sheets_client
        worksheet = get_sheet() # เรียกใช้ Client ที่เราแยกไฟล์ไว้
        worksheet.append_row(row_data) # เพิ่มแถวใหม่
        
        print(f"✅ จดยอดขายสำเร็จ: {menu} | จำนวน: {qty} | รวม: {total_price} บาท")

        # 5. แจ้งเตือนเข้า Telegram
        send_telegram_alert(menu, qty, total_price)
        
    except ValueError:
        print("❌ รูปแบบข้อมูลในเครื่องหมายคำพูดผิด! ต้องเป็น \"เมนู:จำนวน:ราคา\"")
    except Exception as e:
        print(f"❌ บอททำงานพลาด: {e}")

if __name__ == "__main__":
    log_sale()