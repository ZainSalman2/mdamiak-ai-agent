import os
import requests
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# ==========================================
# 1. دالة معالجة النصوص العربية للعرض السليم
# ==========================================
def format_arabic(text):
    """إعادة تشكيل وعكس النص العربي ليظهر متصلاً وسليماً داخل PIL"""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# ==========================================
# 2. دوال النشر والإرسال (Facebook & Telegram)
# ==========================================
def post_to_facebook(page_id, access_token, image_path, caption):
    """رفع المنشور إلى فيسبوك وطباعة الخطأ بدقة في حال وجود نقص بالصلاحيات"""
    url = f"https://graph.facebook.com/v26.0/{page_id}/photos"
    try:
        with open(image_path, "rb") as img_file:
            payload = {
                "caption": caption,
                "access_token": access_token
            }
            files = {"source": img_file}
            response = requests.post(url, data=payload, files=files)
            
        res_data = response.json()
        if response.status_code == 200 and "id" in res_data:
            print(f"✅ تم النشر بنجاح على فيسبوك! Post ID: {res_data['id']}")
            return True
        else:
            err = res_data.get('error', {})
            print(f"❌ خطأ من فيسبوك: [{err.get('code')}] {err.get('message')}")
            if err.get('code') == 200:
                print("💡 تنبيه: الرمز يفتقر إلى صلاحية pages_manage_posts.")
            return False
    except Exception as e:
        print(f"❌ استثناء أثناء النشر على فيسبوك: {e}")
        return False

def send_to_telegram(bot_token, chat_id, image_path, caption):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    try:
        with open(image_path, "rb") as img_file:
            data = {"chat_id": chat_id, "caption": caption}
            files = {"photo": img_file}
            res = requests.post(url, data=data, files=files)
        if res.status_code == 200:
            print("✅ تم إرسال البطاقة إلى تيليجرام بنجاح.")
        else:
            print(f"⚠️ خطأ تيليجرام: {res.text}")
    except Exception as e:
        print(f"❌ استثناء تيليجرام: {e}")

# ==========================================
# 3. محرك توليد التصميم البصري (MdaMiak Card)
# ==========================================
def download_font():
    font_path = "Cairo-Bold.ttf"
    if not os.path.exists(font_path):
        url = "https://raw.githubusercontent.com/google/fonts/main/ofl/cairo/static/Cairo-Bold.ttf"
        r = requests.get(url, timeout=15)
        with open(font_path, "wb") as f:
            f.write(r.content)
    return font_path

def generate_social_card(output_path="output.png"):
    width, height = 1080, 1080
    font_file = download_font()
    
    font_large = ImageFont.truetype(font_file, 52)
    font_medium = ImageFont.truetype(font_file, 34)
    font_small = ImageFont.truetype(font_file, 24)

    img = Image.new("RGB", (width, height), color=(11, 19, 38))
    draw = ImageDraw.Draw(img)

    # إطارات ولمسات الهوية التقنية
    draw.rectangle([(30, 30), (1050, 1050)], outline=(30, 41, 59), width=2)
    draw.rounded_rectangle([(60, 60), (1020, 1020)], radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=3)

    # 1. الترويسة
    header_ar = format_arabic("مِداميك للذكاء الاصطناعي")
    draw.text((960, 110), header_ar, fill=(56, 189, 248), font=font_large, anchor="ra")
    draw.text((120, 115), "MdaMiak AI", fill=(148, 163, 184), font=font_medium)
    draw.line([(100, 200), (980, 200)], fill=(51, 65, 85), width=2)

    # 2. بطاقة المحتوى في المنتصف
    draw.rounded_rectangle([(100, 320), (980, 760)], radius=20, fill=(23, 37, 84), outline=(37, 99, 235), width=2)

    title_ar = format_arabic("أتمتة العمليات الرقمية")
    body_line1 = format_arabic("حوّل مهامك الروتينية المتكررة إلى تدفقات ذكية")
    body_line2 = format_arabic("ارفع كفاءة التشغيل بنسبة تصل إلى 40%")
    body_line3 = format_arabic("حلول مخصصة تعتمد على وكلاء الذكاء الاصطناعي")

    draw.text((540, 400), title_ar, fill=(255, 255, 255), font=font_large, anchor="mm")
    draw.text((540, 510), body_line1, fill=(226, 232, 240), font=font_medium, anchor="mm")
    draw.text((540, 580), body_line2, fill=(56, 189, 248), font=font_medium, anchor="mm")
    draw.text((540, 650), body_line3, fill=(148, 163, 184), font=font_small, anchor="mm")

    # 3. شريط الفوتر
    draw.line([(100, 880), (980, 880)], fill=(51, 65, 85), width=2)
    footer_ar = format_arabic("بناء وتطوير وكلاء الذكاء الاصطناعي | مداميك")
    draw.text((960, 915), footer_ar, fill=(148, 163, 184), font=font_small, anchor="ra")
    draw.text((100, 915), "mdamiak.com", fill=(56, 189, 248), font=font_small)

    img.save(output_path, quality=95)
    print("🎨 تم توليد البطاقة العربية بنجاح.")

# ==========================================
# 4. التنفيذ
# ==========================================
def main():
    fb_page_id = os.getenv("FB_PAGE_ID")
    fb_page_token = os.getenv("FB_PAGE_TOKEN")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    image_path = "output.png"
    generate_social_card(image_path)

    post_caption = """كفاءة أعلى، وقت أسرع، وأخطاء أقل.

في مِداميك نطور لك وكلاء ذكاء اصطناعي مخصصين لأتمتة أعمالك ورفع الكفاءة التشغيلية.

#مِداميك #MdaMiak #أتمتة_الأعمال #ذكاء_اصطناعي #تحول_رقمي"""

    if fb_page_id and fb_page_token:
        print("🚀 محاولة النشر على صفحة فيسبوك...")
        post_to_facebook(fb_page_id, fb_page_token, image_path, post_caption)

    if tg_token and tg_chat_id:
        send_to_telegram(tg_token, tg_chat_id, image_path, post_caption)

if __name__ == "__main__":
    main()
