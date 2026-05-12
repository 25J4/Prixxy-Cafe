# agent_tools.py
from datetime import datetime


def validate_sale(menu: str, quantity: int, price: float) -> None:
    """Guardrails: raise ValueError ถ้าข้อมูลไม่ถูกต้อง"""
    if not menu or not menu.strip():
        raise ValueError("ชื่อเมนูห้ามว่าง")
    if quantity <= 0:
        raise ValueError("จำนวนต้องมากกว่า 0")
    if price <= 0:
        raise ValueError("ราคาต้องมากกว่า 0")


def log_sale(menu: str, quantity: int, price: float) -> dict:
    """บันทึกยอดขาย (เวอร์ชัน fake ต่อกับ Google Sheets ใน step ถัดไป)"""
    validate_sale(menu, quantity, price)
    total = quantity * price
    return {
        "status": "success",
        "menu": menu,
        "quantity": quantity,
        "price": price,
        "total": total,
        "timestamp": datetime.now().isoformat(),
    }


TOOLS = {
    "log_sale": log_sale,
}