# 🥞 Prixxy โตเกียว AI Assistant
![Health Check](https://github.com/25J4/Prixxy-Cafe/actions/workflows/health-check.yml/badge.svg)

ระบบผู้ช่วย AI อัจฉริยะสำหรับร้าน **Prixxy โตเกียว** ที่จะมาเปลี่ยนการสั่งขนมโตเกียวไส้ผสมสุดซับซ้อน ให้กลายเป็นเรื่องง่ายด้วย AI

## 🌟 ปัญหาที่ระบบนี้เข้ามาแก้
ธุรกิจอย่างร้านขนมโตเกียว มักเจอปัญหาลูกค้ารอคิวนาน และการสั่ง **"ไส้ผสมแบบ เลือกได้** (เช่น โตเกียวกะเพรา+ปูอัด+ชีส) ที่คนขายจดออเดอร์พลาดและคำนวณราคายากหากโดนสั่งในรูปแบบที่ไม่เหมือนกัน ระบบนี้จึงถูกพัฒนาขึ้นมาเพื่อรับจบทุกปัญหาหน้าเตา!

อ่านรายละเอียดแนวคิดการออกแบบระบบ (Thinking Process) ได้ที่: [PIVOT.md](PIVOT.md)

## ✨ ฟีเจอร์หลัก (Features)
- **Smart Custom Ordering:** AI สวมบทแม่ค้าร้านโตเกียว เข้าใจบรีฟไส้ผสมสุดแปลก และคำนวณราคาตามเงื่อนไขของร้านได้อย่างแม่นยำ
- **Automated Sales Logger:** บันทึกออเดอร์ลง Google Sheets อัตโนมัติ เพื่อให้ง่ายต่อการทำบัญชีและสรุปยอด
- **Real-time Alert:** ดันแจ้งเตือนออเดอร์เข้ามือถือคนเตรียมของหน้าเตาผ่าน Telegram ทันที
- **Caption Generator:** ระบบช่วยคิดแคปชันโซเชียลมีเดียสไตล์พ่อค้าแม่ค้า สำหรับโปรโมทหน้าร้านและรับงานจัดเลี้ยง (Snack Box)

## 🚀 Live Demo
ลองใช้งานระบบจริงได้ที่นี่: [https://prixxy-cafe.me](https://prixxy-cafe.me)
*(หมายเหตุ: โดเมนนี้เตรียมพร้อมสำหรับการเชื่อมต่อกับระบบคลาวด์ในอนาคต)*

## 🛠️ วิธีติดตั้งและรันในเครื่อง (Local Setup)
1. Clone repository นี้ลงในเครื่อง
2. ติดตั้ง Dependencies ที่จำเป็น: `pip install -r requirements.txt`
3. สร้างไฟล์ `.env` ที่ root folder และใส่ค่าตัวแปรดังนี้:
   ```env
   GOOGLE_API_KEY=your_gemini_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   GOOGLE_SERVICE_ACCOUNT_JSON_B64=your_base64_encoded_json
   GOOGLE_SHEETS_ID=your_google_sheets_id

## Demo Day Self-Check
- [x] Deploy URL ใช้งานได้ (เปิดทดสอบล่าสุด: 16 พฤษภาคม 2026)
- [/] ไม่มี `.env` หรือ `*.json` ใน git history
- [/] PIVOT.md ครบ 3 ข้อ
- [/] README อธิบายระบบของ domain ตัวเอง (ไม่ใช่ MilkLab°)
- [/] knowledge base, prompt, UI ปรับเป็น domain ใหม่หมดแล้ว