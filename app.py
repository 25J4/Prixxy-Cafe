import os
import time
import base64
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# 1. 🚨 โหลด .env ก่อนเป็นอันดับแรกสุด! (ห้ามย้ายบรรทัดนี้ไปไว้หลัง import เครื่องมือเด็ดขาด)
load_dotenv(override=True)

# 2. ค่อย import เครื่องมือและ AI เข้ามา
from google import genai
from rag_engine import RAGEngine
from agent_tools import TOOLS

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-3.1-flash-lite" 

@st.cache_resource
def load_rag():
    return RAGEngine("knowledge/prixxy_tokyo_kb.txt")

rag = load_rag()

# 3. จัดหน้าเว็บให้อยู่กึ่งกลาง
st.set_page_config(page_title="Prixxy Tokyo Web App", page_icon="🥞", layout="centered")

# แทรก CSS เพื่อฟิกซ์กล่องแชทไว้ขอบล่างจอเสมอ
st.markdown("""
    <style>
    /* บังคับกล่องแชทให้อยู่ขอบล่างสุด */
    div[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        padding-bottom: 30px !important;
        padding-top: 15px !important;
        background-color: var(--background-color) !important;
        z-index: 999 !important;
        width: 100% !important;
        max-width: 46rem !important; /* รักษาสัดส่วนความกว้างให้ตรงกับหน้าเว็บ */
    }
    
    /* ดันพื้นที่ด้านล่างสุดของเว็บขึ้น เพื่อไม่ให้กล่องแชทไปบังข้อความแชทบรรทัดสุดท้าย */
    .block-container {
        padding-bottom: 120px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. สร้างแท็บ
tab_home, tab_chat, tab_review, tab_dashboard = st.tabs([
    "🏪 หน้าแรก & เมนู", 
    "🤖 สั่งอาหาร (AI พิกซี่)", 
    "⭐ รีวิวลูกค้า", 
    "📊 ระบบหลังบ้าน"
])

# ==========================================
# แท็บ 1: หน้าแรก และ เมนู
# ==========================================
with tab_home:
    st.title("🥞 Prixxy โตเกียว (Prixxy Tokyo)")
    st.write("📍 พิกัด: หน้า มทร.อีสาน วิทยาเขตขอนแก่น | ⏰ เปิด: จันทร์-เสาร์ (10:00-18:00 น.)")
    st.markdown("---")
    
    st.subheader("📋 เมนูแนะนำ (Menu)")
    
    menu_items = [
        {"image": "img/custard.jpg", "caption": "โตเกียวคัสตาร์ดครีม", "price": "15"},
        {"image": "img/jumbo.jpg", "caption": "โตเกียวจัมโบ้!ไส้กรอกหมูสับปูอัด", "price": "45"},
        {"image": "img/pizza.jpg", "caption": "โตเกียวพิซซ่า", "price": "55"}
    ]
    
    def get_image_base64(path):
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except FileNotFoundError:
            return ""

    st.markdown("""
        <style>
        .menu-item { text-align: center; padding: 15px; border-radius: 20px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .menu-image-container { width: 100%; padding-top: 100%; position: relative; border-radius: 15px; overflow: hidden; margin-bottom: 10px; }
        .menu-image { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; border-radius: 15px; }
        .menu-caption { font-size: 1rem; color: #333; margin: 0; height: 3rem; overflow: hidden; }
        .menu-price { font-size: 1.25rem; color: #ff7f50; font-weight: bold; margin: 0; }
        </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(menu_items):
        with cols[idx % 3]:
            img_base64 = get_image_base64(item["image"])
            if img_base64:
                st.markdown(f'<div class="menu-item"><div class="menu-image-container"><img src="data:image/jpeg;base64,{img_base64}" class="menu-image"></div><p class="menu-caption">{item["caption"]}</p><p class="menu-price">{item["price"]} บาท</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="menu-item"><div class="menu-image-container" style="background-color: #eee;"><div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #888;">ไม่พบรูป</div></div><p class="menu-caption">{item["caption"]}</p><p class="menu-price">{item["price"]} บาท</p></div>', unsafe_allow_html=True)

# ==========================================
# แท็บ 2: ระบบสั่งอาหารกับน้องพิกซี่ (AI Agent)
# ==========================================
with tab_chat:
    st.title("🥞 ผู้ช่วย ของ Prixxy โตเกียว")
    st.caption("สั่งโตเกียวไส้ทะลัก ไส้ผสมสั่งได้ตามใจชอบ หรือสอบถามคิวจัดเลี้ยงได้เลยครับ")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("ถามข้อมูลหรือสั่งเมนูได้เลย..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)

        context_chunks = rag.search(prompt, top_k=3)
        context = "\n---\n".join(context_chunks)

        # คำสั่งให้ AI เข้าใจบทบาท
        instruction = f"""คุณคือ สาว AI ประจำร้าน Prixxy โตเกียว
        - ตอบคำถามลูกค้าจากข้อมูลนี้: {context}
        - หากลูกค้าสั่งโตเกียว (ไม่ว่าจะสั่งเป็นเซ็ต หรือสั่งแบบผสมไส้เอง) ให้คำนวณราคาให้ถูกต้อง และใช้เครื่องมือ 'log_sale' บันทึกออเดอร์ทันที ห้ามแต่งข้อมูลเอง
        - สำคัญมาก: เวลาบันทึกออเดอร์ตรงช่อง menu ให้สรุปรายละเอียดไส้ทั้งหมดที่ลูกค้าสั่งให้ชัดเจน (เช่น 'โตเกียวไข่นก+หมูสับ+ชีส')
        - ถ้าสั่ง แป้งปกติ + ไส้ ➔ เริ่มที่ 10 + ค่าไส้
        - ถ้าสั่ง โตเกียวกะเพรา/พิซซ่า ➔ เริ่มที่ 55 (ไม่ต้องบวก 10 บาทค่าแป้งอีก)
        - ถ้าสั่ง ออปชันพิเศษ ➔ บวกเพิ่มตามขนาด (จัมโบ้ +20)
        - ตอบกลับอย่างเป็นกันเอง สไตล์แม่ค้าสาวสวยใจดี"""

        # --- เริ่มต้นระบบ Auto-Retry ---
        max_retries = 3
        retry_delay = 2 
        response = None

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                    config={
                        "system_instruction": instruction,
                        "tools": [{"function_declarations": [
                            {
                                "name": "log_sale",
                                "description": "ใช้บันทึกออเดอร์และแจ้งเตือนเข้า Telegram เมื่อลูกค้าสั่งขนมโตเกียว",
                                "parameters": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "menu": {"type": "STRING", "description": "ชื่อเมนู"},
                                        "quantity": {"type": "INTEGER", "description": "จำนวนชิ้น"},
                                        "price": {"type": "NUMBER", "description": "ราคาต่อชิ้น (อ้างอิงจากข้อมูลร้าน)"}
                                    },
                                    "required": ["menu", "quantity", "price"]
                                }
                            }
                        ]}]
                    }
                )
                break
                
            except Exception as e:
                error_msg = str(e)
                if "503" in error_msg or "UNAVAILABLE" in error_msg:
                    if attempt < max_retries - 1:
                        with chat_container:
                            with st.spinner(f"เซิร์ฟเวอร์คิวเต็ม กำลังพยายามใหม่รอบที่ {attempt + 1}..."):
                                time.sleep(retry_delay)
                                retry_delay *= 2  
                        continue
                st.error("ขออภัยครับ ตอนนี้เซิร์ฟเวอร์ AI ของ Google คิวเต็มชั่วคราว รบกวนพิมพ์สั่งใหม่อีกครั้งนะครับ 🥺")
                st.stop()
        # --- จบระบบ Auto-Retry ---

        answer = ""
        if response and response.candidates:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    fn_name = part.function_call.name
                    args = part.function_call.args
                    answer = TOOLS[fn_name](**args)
                else:
                    answer = response.text

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with chat_container:
            with st.chat_message("assistant"):
                st.write(answer)

# ==========================================
# แท็บ 3 และ 4: รีวิวลูกค้า และ ระบบหลังบ้าน
# ==========================================
with tab_review:
    st.subheader("⭐ รีวิวความประทับใจจากลูกค้า")
    c1, c2, c3 = st.columns(3)
    c1.success("⭐⭐⭐⭐⭐\n\n**น้องเนย:** แป้งกรอบมากกก ไส้ทะลักสุดๆ สั่งล่วงหน้าผ่านบอทได้ด้วย สะดวกมากค่ะ 🥞✨")
    c2.success("⭐⭐⭐⭐⭐\n\n**พี่เอก:** น้องพิกซี่รับออเดอร์ไวมาก แนะนำไส้ชีสครับ อร่อยแสงออกปาก! 🧀🔥")
    c3.success("⭐⭐⭐⭐⭐\n\n**เจ๊น้ำ:** สั่ง Snack box งานเลี้ยง 30 ชิ้น บอทเตือนเวลาเป๊ะ มารับได้ของร้อนๆ เลย 📦💖")

with tab_dashboard:
    st.subheader("📊 แดชบอร์ดสรุปยอดขาย (Mockup)")
    db1, db2, db3 = st.columns(3)
    db1.metric("ยอดขายวันนี้", "1,250 บาท", "+15% จากเมื่อวาน")
    db2.metric("ออเดอร์ทั้งหมด", "32 ออเดอร์")
    db3.metric("🏆 Best Seller", "ไส้กรอกชีส 🧀", "ขายแล้ว 45 ชิ้น")
    
    st.write("**📈 กราฟยอดขาย 7 วันย้อนหลัง**")
    mock_data = pd.DataFrame({
        "วัน": ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์", "เสาร์", "อาทิตย์"],
        "ยอดขาย": [800, 950, 1100, 1050, 1500, 2100, 1900]
    })
    st.bar_chart(mock_data, x="วัน", y="ยอดขาย", color="#ff7f50")