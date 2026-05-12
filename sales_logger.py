import os
import gspread
from dotenv import load_dotenv
from datetime import datetime # เครื่องมือสำหรับดูดวันที่และเวลาปัจจุบัน

# 1. โหลดการตั้งค่า
load_dotenv()
SHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT_FILE = 'prixxy-cafe-afa01441ab9d.json'

# 2. ยืนยันตัวตนและเปิดตาราง
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
sh = gc.open_by_key(SHEET_ID)
worksheet = sh.sheet1

# 3. สร้างฟังก์ชันสำหรับจดยอดขาย
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
        
    except Exception as e:
        print(f"❌ บอททำงานพลาด: {e}")

if __name__ == "__main__":
    print("กำลังจดยอดขายที่ตารางค้าบ...รอแป๊บ!")
    
    # ลองจำลองการขาย 2 รายการ
    log_sale("คาปูชิโน่เย็น", 2, 60)
    log_sale("ครัวซองต์เนยสด", 1, 45)