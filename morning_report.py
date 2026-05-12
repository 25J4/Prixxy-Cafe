import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sheets_client import get_sheet

#โหลดการตั้งค่า
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_morning_report():
    try:
        #อ่านข้อมูลทั้งหมดจาก Google Sheet
        sheet = get_sheet()
        all_data = sheet.get_all_records() # ดึงข้อมูลออกมาเป็น List ของ Dictionary

        if not all_data:
            print("⚠️ ไม่มีข้อมูลในตารางเลยครับผม!")
            return

        #กรองเฉพาะยอดขายของ "เมื่อวาน"
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_sales = [row for row in all_data if row['วันที่'].startswith(yesterday)]

        if not yesterday_sales:
            message = f"☀️ มอนิ่งค้าบ! เมื่อวาน ({yesterday})\nร้านเราเงียบเหงาจัง ไม่มีออเดอร์เลยครับ 🥲"
        else:
            total_revenue = sum(row['ยอดรวม'] for row in yesterday_sales)
            total_orders = len(yesterday_sales)
            
            #นับจำนวนแยกตามเมนู
            menu_counts = {}
            for row in yesterday_sales:
                menu = row['เมนู']
                menu_counts[menu] = menu_counts.get(menu, 0) + row['จำนวน']
            
            #เรียงลำดับจากขายดีมากไปน้อย
            sorted_menus = sorted(menu_counts.items(), key=lambda x: x[1], reverse=True)
            
            #เตรียมรายการแบบ 1. 2. 3. 4.
            menu_list_text = ""
            for i, (menu, qty) in enumerate(sorted_menus, 1):
                menu_list_text += f"{i}. {menu} จำนวน {qty} ชิ้น\n"
            
            #หา Best Seller (อันดับ 1)
            best_seller_name = sorted_menus[0][0]
            best_seller_qty = sorted_menus[0][1]

            #ร่างข้อความใหม่ตามบรีฟ
            message = (
                f"☀️ *มอนิ่งครับ! สรุปยอดเมื่อวานมาแล้วจ้า* ☀️\n"
                f"--------------------------------------\n"
                f"📅 วันที่: {yesterday}\n"
                f"💰 ยอดรวมรายได้: *{total_revenue:,.2f}* บาท\n"
                f"🏆 Best Seller: *{best_seller_name}* ({best_seller_qty} ชิ้น)\n"
                f"--------------------------------------\n"
                f"📊 รายการสินค้าที่ขายออกเมื่อวาน:\n"
                f"{menu_list_text}"
                f"--------------------------------------\n"
                f"📦 จำนวนออเดอร์ทั้งหมด: {total_orders} รายการ\n\n"
                f"วันนี้ลุยกันต่อ ขอให้ลูกค้าเต็มร้านนะค้าบ! 🚀☕"
            )

        #ส่งไปที่ Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, data=payload)
        print(f"📱 ส่งสรุปยอดเมื่อวาน ({yesterday}) เข้า Telegram เรียบร้อย!")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการทำรายงาน: {e}")

if __name__ == "__main__":
    send_morning_report()