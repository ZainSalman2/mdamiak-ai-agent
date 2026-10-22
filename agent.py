import os
import sys
import json
import random
import urllib.parse
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# 1. إعداد الاتصال المباشر بـ Gemini REST API (مضمون 100% بدون مشاكل مكتبات)
api_key = os.environ.get("GEMINI_API_KEY", "").strip()
if not api_key:
    print("❌ خطأ: مفتاح GEMINI_API_KEY غير موجود في GitHub Secrets!")
    sys.exit(1)

topics = [
    "أداة ذكاء اصطناعي مجانية توفر ساعات من العمل",
    "فكرة أتمتة ذكية لربط الواتساب وجداول البيانات لأصحاب المشاريع",
    "قاعدة ذهبية في هندسة الأوامر (Prompt Engineering) للحصول على نتائج احترافية",
    "كيف تقلل تكاليف التشغيل في مشروعك باستخدام وكلاء الذكاء الاصطناعي",
    "خطأ شائع يقع فيه رواد الأعمال عند استخدام الذكاء الاصطناعي وكيفية تجنبه"
]
selected_topic = random.choice(topics)

prompt = f"""
أنت المدير الإبداعي لعلامة (مَداميك | MdaMiak) المتخصصة في الأتمتة، وكلاء الذكاء الاصطناعي، والحلول الرقمية للأعمال.
اكتب منشوراً جديداً ومبتكراً لفيسبوك وانستجرام حول هذا الموضوع تحديداً: ({selected_topic}).
أخرج النتيجة بصيغة JSON فقط بدون أي نص إضافي، تحتوي على المفاتيح التالية:
{{
  "headline": "عنوان عربي قوي وخاطف للانتباه بدون تشكيل (من 5 إلى 7 كلمات فقط)",
  "caption": "نص المنشور الكامل بأسلوب احترافي مع نقاط واضحة وسؤال تفاعلي في النهاية والهاشتاجات المناسبة",
  "image_prompt": "Futuristic luxury dark navy and cyan 3D isometric technology background, glowing digital nodes and abstract geometric blocks, sleek minimalist corporate style, 8k, no text"
}}
"""

print("1. جاري توليد فكرة ونص المنشور عبر Gemini...")
data = None
models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

for model_name in models:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        res = requests.post(url, json=payload, timeout=30)
        if res.status_code == 200:
            res_json = res.json()
            raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            if "```" in raw_text:
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            data = json.loads(raw_text.strip())
            print(f"✅ تم التوليد بنجاح عبر نموذج: {model_name}")
            break
        else:
            print(f"⚠️ استجابة غير متوقعة من {model_name}: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"⚠️ خطأ أثناء الاتصال بـ {model_name}: {e}")

if not data:
    print("⚠️ تم استخدام المحتوى الاحتياطي نظراً لتعذر الاتصال بـ Gemini.")
    data = {
        "headline": "أتمتة المهام: سلاحك السري لمضاعفة أرباحك",
        "caption": "في مَداميك | MdaMiak نحول المهام اليومية المتكررة إلى أنظمة ذكية تعمل تلقائياً بدقة وسرعة.\n\n🔹 توفير 70% من وقت الفريق\n🔹 تقليل الأخطاء البشرية إلى الصفر\n🔹 خدمة عملاء فورية على مدار الساعة\n\nما هي المهمة التي تستهلك معظم وقتك حالياً؟ شاركنا في التعليقات! 👇\n\n#مداميك #MdaMiak #ذكاء_اصطناعي #أتمتة_الأعمال",
        "image_prompt": "Futuristic luxury dark tech background glowing cyan geometric blocks"
    }

headline = data.get("headline", "حلول الأتمتة الذكية من مداميك")
caption = data.get("caption", "")
image_prompt = data.get("image_prompt", "Futuristic dark tech background")

# 2. توليد الخلفية البصرية مع قص ديناميكي يملأ الشاشة بالكامل ويزيل العلامة المائية
print("2. جاري توليد الخلفية البصرية...")
bg_image = None
try:
    seed = random.randint(1000, 999999)
    encoded_prompt = urllib.parse.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true&seed={seed}"
    img_response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=45)
    if img_response.status_code == 200 and len(img_response.content) > 1000:
        raw_img = Image.open(BytesIO(img_response.content)).convert("RGBA")
        w, h = raw_img.size
        # قص 8% من الحواف चारों لإزالة أي شعار مائي مهما كان مقاس الصورة الأصلي ثم تكبيرها لـ 1080x1080
        margin_w, margin_h = int(w * 0.08), int(h * 0.08)
        bg_image = raw_img.crop((margin_w, margin_h, w - margin_w, h - margin_h)).resize((1080, 1080), Image.Resampling.LANCZOS)
        print("✅ تم توليد الخلفية وملء الأبعاد بالكامل بدون علامة مائية!")
except Exception as e:
    print(f"⚠️ تعذر جلب الصورة الخارجية: {e}")

if bg_image is None:
    bg_image = Image.new("RGBA", (1080, 1080), (10, 18, 36, 255))

# طبقة تظليل فخمة لإبراز النص العربي بوضوح عالٍ
overlay = Image.new("RGBA", (1080, 1080), (6, 12, 28, 185))
final_img = Image.alpha_composite(bg_image, overlay).convert("RGB")
draw = ImageDraw.Draw(final_img)

# 3. تحميل الخط العربي (Tajawal Bold)
print("3. جاري تحميل الخط العربي وتصميم البطاقة...")
font_url = "https://github.com/google/fonts/raw/main/ofl/tajawal/Tajawal-Bold.ttf"
font_bytes = requests.get(font_url, timeout=20).content

title_font = ImageFont.truetype(BytesIO(font_bytes), 64, layout_engine=ImageFont.Layout.RAQM)
brand_font = ImageFont.truetype(BytesIO(font_bytes), 42, layout_engine=ImageFont.Layout.RAQM)
footer_font = ImageFont.truetype(BytesIO(font_bytes), 30, layout_engine=ImageFont.Layout.RAQM)

# 4. رسم الإطار والهوية البصرية (مداميك | MdaMiak)
draw.rectangle([(55, 55), (1025, 1025)], outline=(0, 210, 255), width=2)
draw.text((540, 130), "مداميك | MdaMiak", font=brand_font, fill=(0, 210, 255), anchor="mm", direction="rtl")
draw.line([(380, 175), (700, 175)], fill=(0, 210, 255), width=3)

# 5. تقسيم وطباعة العنوان الرئيسي في المنتصف
words = headline.split()
lines, current_line = [], []
for word in words:
    current_line.append(word)
    if len(current_line) >= 3:
        lines.append(" ".join(current_line))
        current_line = []
if current_line:
    lines.append(" ".join(current_line))

y_pos = 510 - (len(lines) * 45)
for line in lines:
    draw.text((540, y_pos), line, font=title_font, fill=(255, 255, 255), anchor="mm", direction="rtl")
    y_pos += 105

# 6. طباعة التوقيع السفلي
draw.text((540, 955), "نبني مستقبلك الرقمي بذكاء | @MdaMiak", font=footer_font, fill=(180, 200, 225), anchor="mm", direction="rtl")

# 7. حفظ المخرجات
os.makedirs("output", exist_ok=True)
final_img.save("output/post_image.jpg", quality=95)
with open("output/caption.txt", "w", encoding="utf-8") as f:
    f.write(caption)

print("🎉 تم إنتاج التصميم والمنشور الجديد بنجاح!")
