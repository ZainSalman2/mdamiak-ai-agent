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
# 2. الدالة الرئيسية (توليد، تصميم، ونشر)
# ==========================================

def main():
    # 1. استدعاء المفاتيح من بيئة التشغيل (GitHub Secrets)
    gemini_key = os.getenv("GEMINI_API_KEY")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    fb_page_id = os.getenv("FB_PAGE_ID")
    fb_page_token = os.getenv("FB_PAGE_TOKEN")

    image_path = "output.png"
    
    # 2. توليد المحتوى والتصميم (تأكد من وجود الكود الخاص بك هنا لتوليد output.png و post_text)
    # مثال للمحتوى النصي:
    post_text = (
        "
