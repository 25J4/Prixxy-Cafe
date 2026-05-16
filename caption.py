import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# โหลด .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-3.1-flash-lite"

st.title("✍️ นักการตลาด AI - Prixxy โตเกียว")
st.caption("ตัวช่วยคิดแคปชันโซเชียลมีเดีย สำหรับโปรโมทหน้าร้านและรับจัด Snack Box")

topic = st.text_input("วันนี้อยากโปรโมทอะไรครับ?", placeholder="เช่น โตเกียวกะเพราชีส, เซ็ตวัยรุ่นย้อนยุค, หรือรับเหมาเตาจัดเลี้ยง")
tone = st.selectbox("เลือก Mood & Tone", [
    "สนุกสนาน เป็นกันเอง ชวนหิว", 
    "ทางการ น่าเชื่อถือ", 
    "กวนๆ สไตล์พ่อค้าสตรีทฟู้ด"
])

if st.button("✨ เจนแคปชันเลย!"):
    if topic:
        # คำสั่ง Prompt สำหรับร้านโตเกียว
        prompt = f"""
        คุณคือ Content Creator มืออาชีพของร้าน 'Prixxy โตเกียว'
        จงเขียนแคปชันโซเชียลมีเดียเพื่อโปรโมท: {topic}
        Mood & Tone: {tone}
        
        ข้อมูลจุดขายของร้าน: 
        - ร้านขนมโตเกียวพรีเมียม แป้งหอมกรอบนุ่ม (ออริจินัล วนิลา, ชาโคล)
        - จุดเด่นคือ 'เลือกไส้ผสมได้ตามใจชอบ' มีทั้งไส้คาว หวาน และออปชันพรีเมียม
        - มีบริการรับจัด Snack Box ขั้นต่ำ 50 กล่อง และบริการเหมาเตาไปทอดสดหน้างาน
        
        ข้อบังคับ:
        - เขียนให้กระชับ น่าอ่าน ใช้ Emoji ประกอบให้ดูน่ากิน
        - ใส่ Call to Action ให้ทักแชทสั่งล่วงหน้าได้
        - ใส่ Hashtag ท้ายข้อความ: #Prixxyโตเกียว #โตเกียวไส้ทะลัก #SnackBox #รับจัดเบรค
        - ตอบกลับเฉพาะส่วนที่เป็นเนื้อหาแคปชันเท่านั้น ไม่ต้องอารัมภบท
        """
        
        with st.spinner("กำลังปั่นแคปชันหอมๆ..."):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )
                st.success("เสร็จเรียบร้อย! คัดลอกไปโพสต์ได้เลยครับ 🚀")
                st.write(response.text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {str(e)}")
    else:
        st.warning("กรุณาใส่หัวข้อที่อยากโปรโมทก่อนนะครับ!")