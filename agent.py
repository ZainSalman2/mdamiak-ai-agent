import os
import requests
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. دوال النشر والإرسال
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
            error_details = result.get('error', {})
            error_msg = error_details.get('message', 'خطأ غير معروف')
            error_code = error_details.get('code', 'N/A')
            print(f"❌ فشل النشر على فيسبوك | كود الخطأ: {error_code} | الرسالة: {error_msg}")
    except Exception as e:
        print(f"❌ استثناء تقني أثناء النشر على فيسبوك: {e}")

def send_to_telegram(bot_token, chat_id, image_path, caption):
    """إرسال نسخة للمعاينة عبر تيليجرام"""
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    try:
        with open(image_path, "rb") as img_file:
            data = {"chat_id": chat_id, "caption": caption}
            files = {"photo": img_file}
            res = requests.post(url, data=data, files=files)
        if res.status_code == 200:
            print("✅ تم إرسال المعاينة إلى تيليجرام بنجاح.")
        else:
            print(f"⚠️ خطأ تيليجرام: {res.text}")
    except Exception as e:
        print(f"❌ استثناء تيليجرام: {e}")

# ==========================================
# 2. إنشاء وتنسيق التصميم الاحترافي
# ==========================================

def download_arabic_font():
    """تحميل خط عربي حديث (Tajawal) تلقائياً إذا لم يكن متوفراً"""
    font_path = "Tajawal-Bold.ttf"
    if not os.path.exists(font_path):
        url = "https://raw.githubusercontent.com/google/fonts/main/ofl/tajawal/Tajawal-Bold.ttf"
        r = requests.get(url, timeout=15)
        with open(font_path, "wb") as f:
            f.write(r.content)
    return font_path

def generate_branded_image(title, body_text, output_path="output.png"):
    """توليد تصميم احترافي متناسق بهوية مِداميك"""
    width, height = 1080, 1080
    
    # 1. إنشاء الخلفية بتدرج داكن فخم
    img = Image.new("RGB", (width, height), color=(10, 15, 29))
    draw = ImageDraw.Draw(img)

    # إضافة لمسات جمالية للخلفية (توهج وإطارات)
    draw.rectangle([(40, 40), (1040, 1040)], outline=(30, 41, 59), width=2)
    draw.rounded_rectangle([(70, 70), (1010, 1010)], radius=24, fill=(17, 24, 39), outline=(56, 189, 248), width=3)

    # 2. تحميل الخطوط
    font_file = download_arabic_font()
    try:
        font_brand = ImageFont.truetype(font_file, 48)
        font_title = ImageFont.truetype(font_file, 56)
        font_body = ImageFont.truetype(font_file, 34)
        font_footer = ImageFont.truetype(font_file, 26)
    except Exception:
        font_brand = font_title = font_body = font_footer = ImageFont.load_default()

    # 3. الهيدر (الشعار واسم العلامة)
    draw.text((120, 120), "مِداميك | MdaMiak", fill=(56, 189, 248), font=font_brand)
    draw.text((120, 185), "حلول أتمتة الأعمال والذكاء الاصطناعي", fill=(148, 163, 184), font=font_footer)
    draw.line([(120, 235), (960, 235)], fill=(51, 65, 85), width=2)

    # 4. العنوان الرئيسي
    draw.text((120, 360), title, fill=(248, 250, 252), font=font_title)

    # 5. محتوى النصيحة / القيمة التسويقية
    draw.rounded_rectangle([(120, 480), (960, 780)], radius=16, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
    
    # كتابة نص المحتوى داخل البطاقة الداخلية
    draw.text((150, 530), body_text, fill=(203, 213, 225), font=font_body, spacing=14)

    # 6. الفوتر (شريط التواصل)
    draw.line([(120, 890), (960, 890)], fill=(51, 65, 85), width=2)
    draw.text((120, 920), "mdamiak.com", fill=(56, 189, 248), font=font_footer)
    draw.text((680, 920), "نحو تحول رقمي ذكي ومستدام", fill=(148, 163, 184), font=font_footer)

    img.save(output_path, quality=95)
    print("🎨 تم إنشاء التصميم الاحترافي بنجاح: output.png")

# ==========================================
# 3. الدالة الرئيسية
# ==========================================

def main():
    fb_page_id = os.getenv("FB_PAGE_ID")
    fb_page_token = os.getenv("FB_PAGE_TOKEN")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    image_path = "output.png"

    # النصوص المخصصة للتصميم
    card_title = "هل تعلم كيف توفر أتمتة الأعمال 40% من وقت فريقك؟"
    card_body = (
        "دمج وكلاء الذكاء الاصطناعي المخصصين يتولى المهام الروتينية المتكررة\n"
        "بما فيها إدخال البيانات، التوثيق، والتواصل المباشر مع العملاء\n"
        "ليركز فريقك على الابتكار ونمو الأعمال الفعلي."
    )

    # إنشاء التصميم المطور
    generate_branded_image(card_title, card_body, image_path)

    post_caption = """كفاءة أعلى، وقت أسرع، وأخطاء أقل.

في مِداميك، نبني ونطور حلول أتمتة ذكية مدعومة بنماذج الذكاء الاصطناعي التوليدي لمساعدة الشركات على إدارة وتسيير أعمالها بسلاسة تامة.

ما هي أكثر مهمة روتينية تتمنى أتمتتها في عملك اليوم؟

#مِداميك #MdaMiak #أتمتة_الأعمال #ذكاء_اصطناعي #تحول_رقمي"""

    # محاولة النشر على فيسبوك
    if fb_page_id and fb_page_token:
        print("🚀 جارٍ النشر التلقائي على صفحة فيسبوك...")
        post_to_facebook(fb_page_id, fb_page_token, image_path, post_caption)
    else:
        print("⚠️ لم يتم العثور على بيانات الربط الخاصة بفيسبوك.")

    # إرسال المعاينة لتيليجرام
    if tg_token and tg_chat_id:
        print("📲 جارٍ إرسال المعاينة لتيليجرام...")
        send_to_telegram(tg_token, tg_chat_id, image_path, post_caption)

if __name__ == "__main__":
    main()
