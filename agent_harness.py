# agent_harness.py
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from agent_tools import TOOLS

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """คุณคือ ผู้ช่วย AI ของร้าน Prixxy-Cafe
หน้าที่ของคุณคือแปลงคำสั่งภาษาไทยเป็น JSON action
ตอบกลับเป็น JSON เท่านั้น ในรูปแบบ:
{"action": "log_sale", "args": {"menu": "...", "quantity": N, "price": N}}
ถ้าคำสั่งไม่ใช่การบันทึกยอดขาย ตอบ: {"action": "unknown", "args": {}}"""

TRACE_FILE = "agent_trace.log"


def write_trace(event: str, data: dict) -> None:
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            **data,
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_agent(user_input: str) -> str:
    write_trace("user_input", {"message": user_input})

    response = client.models.generate_content(
        model=MODEL,
        contents=f"{SYSTEM_INSTRUCTION}\n\nคำสั่ง: {user_input}",
    )
    raw = response.text.strip()
    write_trace("llm_response", {"raw": raw})
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        action_data = json.loads(raw)
    except json.JSONDecodeError:
        return "❌ AI ตอบกลับในรูปแบบที่ไม่ถูกต้อง"

    action = action_data.get("action")
    args = action_data.get("args", {})

    if action not in TOOLS:
        return f"⚠️ ไม่รู้จัก action: {action}"

    try:
        result = TOOLS[action](**args)
        write_trace("tool_result", {"action": action, "result": result})
        return (
            f"✅ บันทึกสำเร็จ: {result['menu']} "
            f"x{result['quantity']} = {result['total']} บาท"
        )
    except (ValueError, TypeError) as e:
        write_trace("tool_error", {"action": action, "error": str(e)})
        return f"❌ ข้อมูลไม่ถูกต้อง: {e}"


if __name__ == "__main__":
    print("Demi Agent พร้อมรับคำสั่ง (พิมพ์ 'exit' เพื่อออก)\n")
    while True:
        user_input = input("คุณ: ").strip()
        if user_input.lower() == "exit":
            break
        print(f"Demi: {run_agent(user_input)}\n")