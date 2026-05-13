import os
import requests
from datetime import datetime

def validate_sale(menu: str, quantity: int, price: float) -> None:
    """Guardrails: ป้องกันข้อมูลแปลกปลอม"""
    if not menu or not menu.strip():
        raise ValueError("ชื่อเมนูห้ามว่าง")
    if quantity <= 0:
        raise ValueError("จำนวนต้องมากกว่า 0")
    if price <= 0:
        raise ValueError("ราคาต้องมากกว่า 0")

def log_sale(menu: str, quantity: int, price: float) -> str:
    """บันทึกออเดอร์และแจ้งเตือนผ่าน Telegram"""
    try:
        validate_sale(menu, quantity, price)
    except ValueError as e:
        return f"ข้อมูลออเดอร์ไม่ถูกต้องครับ: {str(e)}"

    total = quantity * price
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message = (
        f"🔔 **ออเดอร์ใหม่จาก Prixxy-Cafe!**\n"
        f"📅 เวลา: {timestamp}\n"
        f"☕ เมนู: {menu}\n"
        f"🔢 จำนวน: {quantity} แก้ว\n"
        f"💰 ยอดรวม: {total} บาท\n"
        f"------------------------"
    )
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return f"รับออเดอร์ {menu} เรียบร้อย! (โหมดทดสอบ: ยังไม่ได้ใส่ Telegram Token)"

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return f"รับออเดอร์ '{menu}' จำนวน {quantity} แก้ว เรียบร้อยครับ ส่งออเดอร์เข้าบาร์น้ำแล้ว!"
        else:
            return f"รับออเดอร์แล้วครับ แต่ระบบหลังบ้านติดขัดนิดหน่อย (Error: {response.status_code})"
    except Exception as e:
        return f"รับออเดอร์แล้ว แต่เกิดปัญหาการแจ้งเตือน: {str(e)}"

TOOLS = {
    "log_sale": log_sale,
}