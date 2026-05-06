import os
from dotenv import load_dotenv
import google.generativeai as genai

# โหลด Environment Variables จากไฟล์ .env
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    print("❌ หา GOOGLE_API_KEY ไม่เจอ ตรวจสอบไฟล์ .env ด่วนครับ!")
    exit()

# ตั้งค่า API Key ให้กับ Google SDK
genai.configure(api_key=GOOGLE_API_KEY)

def generate_captions(menu_name, price):
    # ใช้โมเดล Gemini 2.5 Flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # อัปเดต Prompt ให้ใส่ชื่อร้าน Prixxy-Cafe ลงไป
    prompt = (
        f"Generate 3 Instagram caption variants for 'Prixxy-Cafe' featuring '{menu_name}' priced at {price}. "
        "The captions should be in three distinct styles: cute, minimal, and gen-z. "
        "Please provide the output in Thai, output each caption on a new line, and clearly number them. "
        "Make sure to include the cafe name '#PrixxyCafe' in the hashtags."
    )
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # จัดการข้อความให้ออกมาเป็น List คลีนๆ
        captions = [line.strip() for line in text.split('\n') if line.strip()]
        return captions
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดในการเรียกใช้ API: {e}")
        return []

if __name__ == "__main__":
    # ลองเปลี่ยนเมนูเทสดูบ้าง
    sample_menu = "สตรอว์เบอร์รีโซดา (Strawberry Soda)"
    sample_price = "75 บาท"
    
    print(f"🚀 กำลังให้ AI คิด Caption สำหรับ {sample_menu} ร้าน Prixxy-Cafe...")
    captions = generate_captions(sample_menu, sample_price)
    
    if not captions:
        print("⚠️ ไม่สามารถสร้าง Caption ได้ครับ")
    else:
        print("\n✨ ผลลัพธ์ Caption สไตล์ Prixxy-Cafe:")
        for caption in captions:
            print(caption)