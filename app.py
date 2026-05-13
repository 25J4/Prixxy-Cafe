import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from rag_engine import RAGEngine
from agent_tools import TOOLS

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-3.1-flash-lite" 

@st.cache_resource
def load_rag():
    return RAGEngine("knowledge/prixxy_kb.txt")

rag = load_rag()

st.title("☕ Prixxy ผู้ช่วย AI ของ Prixxy-Cafe")
st.caption("สอบถามข้อมูลร้าน หรือสั่งเครื่องดื่มได้เลยครับ")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("ถามข้อมูลหรือสั่งเมนูได้เลย..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # ดึงบริบทจาก RAG
    context_chunks = rag.search(prompt, top_k=3)
    context = "\n---\n".join(context_chunks)

    # คำสั่งให้ AI เข้าใจบทบาท (System Instruction)
    instruction = f"""คุณคือ Prixxy AI ประจำร้าน Prixxy-Cafe
    - ตอบคำถามลูกค้าจากข้อมูลนี้: {context}
    - หากลูกค้า 'สั่งซื้อเครื่องดื่ม' ให้คุณใช้เครื่องมือ 'log_sale' บันทึกออเดอร์ทันที ห้ามแต่งข้อมูลเอง
    - ตอบกลับอย่างเป็นกันเองและสุภาพ"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "system_instruction": instruction,
            "tools": [{"function_declarations": [
                {
                    "name": "log_sale",
                    "description": "ใช้บันทึกออเดอร์และแจ้งเตือนเข้า Telegram เมื่อลูกค้าสั่งเครื่องดื่ม",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "menu": {"type": "STRING", "description": "ชื่อเมนู"},
                            "quantity": {"type": "INTEGER", "description": "จำนวนแก้ว"},
                            "price": {"type": "NUMBER", "description": "ราคาต่อแก้ว (อ้างอิงจากข้อมูลร้าน)"}
                        },
                        "required": ["menu", "quantity", "price"]
                    }
                }
            ]}]
        }
    )

    # ตรวจสอบการเรียกใช้ Tools
    answer = ""
    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn_name = part.function_call.name
            args = part.function_call.args
            # รัน Tool ส่ง Telegram
            answer = TOOLS[fn_name](**args)
        else:
            answer = response.text

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)