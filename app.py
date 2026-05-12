# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from rag_engine import RAGEngine # เรียกใช้ Engine จากไฟล์ที่เราสร้าง

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"

# โหลดฐานความรู้ของร้าน Prixxy-Cafe
@st.cache_resource
def load_rag():
    # ตรวจสอบว่ามีไฟล์ในโฟลเดอร์ knowledge/prixxy_kb.txt จริงๆ นะครับ
    return RAGEngine("knowledge/prixxy_kb.txt")

rag = load_rag()

st.title("☕ Prixxy ผู้ช่วย AI ของ Prixxy-Cafe")
st.caption("ถามเรื่องเมนู เวลาเปิด หรือข้อมูลร้านได้เลย")

if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติการแชท
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ช่องรับคำถาม
if prompt := st.chat_input("ถามอะไรเกี่ยวกับร้านได้เลย..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # RAG: Search (ค้นหาข้อมูลที่ใกล้เคียงที่สุด 3 ส่วน)
    context_chunks = rag.search(prompt, top_k=3)
    context = "\n---\n".join(context_chunks)

    # Generate (สร้างคำตอบโดยบังคับให้อ่านจากข้อมูลที่เราค้นเจอ)
    full_prompt = f"""คุณคือ Prixxy ผู้ช่วย AI ของร้าน Prixxy-Cafe 
ตอบเฉพาะจากข้อมูลด้านล่างเท่านั้น ถ้าไม่พบข้อมูล ให้บอกว่าไม่ทราบ อย่าแต่งข้อมูลเอง
ข้อมูลร้าน:
{context}

คำถาม: {prompt}"""

    response = client.models.generate_content(model=MODEL, contents=full_prompt)
    answer = response.text
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)