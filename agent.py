import os
import requests
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. دوال النشر والإرسال (Facebook & Telegram)
# ==========================================

def post_to_facebook(page_id, access_token, image_path, caption):
    """رفع الصورة والنص التسويقي مباشرة إلى صفحة فيسبوك عبر Meta Graph API"""
    url = f"https://graph.facebook.com/v26.0/{page_id}/photos"
    try:
        with open(image_path, "rb") as img_file:
            payload = {
                "caption": caption,
                "access_token": access_token
            }
            files = {
                "source": img_file
            }
            response = requests.post(url, data=payload, files=files)
            
        result = response.json()
        if response.status_code == 200 and "id" in result:
            print(f"✅ تم النشر بنجاح على فيسبوك! معرف المنشور: {result['id']}")
        else:
            error_msg = result.get('error', {}).get('message', 'خطأ غير معروف')
            print(f"❌ فشل النشر على فيسبوك: {error_msg}")
    except Exception as e:
        print(f"❌ استثناء أثناء النشر على فيسبوك: {e}")

def send_to_telegram(bot_token, chat_id, image_path, caption):
    """إرسال نسخة احتياطية من البطاقة والنص إلى بوت تيليجرام"""
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    try:
        with open(image_path, "rb") as img_file:
            data = {"chat_id": chat_id, "caption": caption}
            files = {"photo": img_file}
            res = requests.post(url, data=data, files=files)
        if res.status_code == 200:
            print("✅ تم إرسال النسخة الاحتياطية إلى تيليجرام بنجاح.")
        else:
            print(f"⚠️ خطأ في إرسال تيليجرام: {res.text}")
    except Exception as e:
        print(f"❌ استثناء أثناء إرسال تيليجرام: {e}")

# ==========================================
# 2. توليد صورة تجريبية
# ==========================================

def create_sample_image(output_path="output.png"):
    """إنشاء بطاقة بصرية تجريبية لعلامة مداميك"""
    img = Image.new("RGB", (1080, 1080), color=(15, 23, 42))  # خلفية داكنة فخمة
    draw = ImageDraw.Draw(img)
    
    # رسم إطار وبطاقة في المنتصف
    draw.rectangle([(80, 80), (1000, 1000)], outline=(56, 189, 248), width=4)
    
    # نص تجريبي على التصميم
    text = "MdaMiak | مداميك\nAI Automation Solutions"
    draw.text((260, 500), text, fill=(255, 255, 255))
    
    img.save(output_path)
    print("🎨 تم إنشاء الصورة بنجاح: output.png")

# ==========================================
# 3. الدالة الرئيسية (Main)
# ==========================================

def main():
    gemini_key = os.getenv("GEMINI_API_KEY")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    fb_page_id = os.getenv("FB_PAGE_ID")
    fb_page_token = os.getenv("FB_PAGE_TOKEN")

    image_path = "output.png"
    
    # 1. إنشاء الصورة
    create_sample_image(image_path)

    # 2. النص التسويقي
    post_text = """مستقبل أعمالك يبدأ بالأتمتة الذكية.

في مِداميك نطور لك وكلاء ذكاء اصطناعي مخصصين لرفع الكفاءة وتوفير الوقت والموارد.

#مداميك #MdaMiak #ذكاء_اصطناعي #أتمتة_الأعمال"""

    # 3. النشر التلقائي على صفحة فيسبوك
    if fb_page_id and fb_page_token:
        print("🚀 جارٍ النشر التلقائي على صفحة فيسبوك (MdaMiak)...")
        post_to_facebook(fb_page_id, fb_page_token, image_path, post_text)
    else:
        print("⚠️ لم يتم العثور على مفاتيح فيسبوك في Secrets.")

    # 4. إرسال النسخة إلى تيليجرام
    if tg_token and tg_chat_id:
        print("📲 جارٍ إرسال الإشعار والبطاقة إلى تيليجرام...")
        send_to_telegram(tg_token, tg_chat_id, image_path, post_text)

if __name__ == "__main__":
    main()
