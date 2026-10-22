import os
import sys
import json
import random
import urllib.parse
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from google import genai

# 1. إعداد الاتصال بـ Gemini API
api_key = os.environ.get("GEMINI_API_KEY", "").strip()
if not api_key:
    print("❌ خطأ: مفتاح GEMINI_API_KEY غير موجود!")
    sys.exit(1)

client = genai.Client(api_key=api_key)

prompt = """
أنت المدير الإبداعي لعلامة (مَداميك | MdaMiak) المتخصصة في الأتمتة، وكلاء الذكاء الاصطناعي، والحلول الرقمية للأعمال.
ابتكر منشوراً احترافياً وجذاباً لفيسبوك وانستجرام يقدم أداة ذكية أو فكرة أتمتة عملية تزيد الإنتاجية.
أخرج النتيجة بصيغة JSON فقط بدون أي نص إضافي، تحتوي على المفاتيح التالية:
{
  "headline": "عنوان عربي قوي وخاطف للانتباه بدون تشكيل (من 5 إلى 7 كلمات)",
  "caption": "نص المنشور الكامل بأسلوب احترافي مع نقاط واضحة وسؤال تفاعلي في النهاية والهاشتاجات",
  "image_prompt": "Futuristic luxury dark tech background, glowing cyan and gold 3D geometric blocks, depth of field, minimalist, dark navy lighting, 8k, no text"
}
"""

print("1. جاري توليد فكرة ونص المنشور عبر Gemini...")
data = None
for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        raw_text = response.text.strip()
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        data = json.loads(raw_text.strip())
        print(f"✅ تم التوليد بنجاح عبر نموذج: {model_name}")
        break
    except Exception as e:
        print(f"⚠️ محاولة النموذج {model_name} لم تكتمل: {e}")

if not data:
    data = {
        "headline": "أتمتة المهام: سلاحك السري لمضاعفة أرباحك",
        "caption": "في مَداميك | MdaMiak نحول المهام اليومية المتكررة إلى أنظمة ذكية تعمل تلقائياً بدقة وسرعة.\n\n🔹 توفير 70% من وقت الفريق\n🔹 تقليل الأخطاء البشرية إلى الصفر\n🔹 خدمة عملاء فورية على مدار الساعة\n\nما هي المهمة التي تستهلك معظم وقتك حالياً؟ شاركنا في التعليقات! 👇\n\n#مداميك #MdaMiak #ذكاء_اصطناعي #أتمتة_الأعمال",
        "image_prompt": "Futuristic luxury dark tech background glowing cyan geometric blocks"
    }

headline = data.get("headline", "حلول الأتمتة الذكية من مداميك")
caption = data.get("caption", "")
image_prompt = data.get("image_prompt", "Futuristic dark tech background")

# 2. توليد الخلفية البصرية وقص العلامة المائية تلقائياً
print("2. جاري توليد الخلفية البصرية...")
bg_image = None
try:
    seed = random.randint(100, 99999)
    encoded_prompt = urllib.parse.quote(image_prompt)
    # نطلب صورة أكبر قليلاً (1160x1160) لنقص الحواف ونزيل شعار pollinations.ai تماماً
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1160&height=1160&nologo=true&seed={seed}"
    img_response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=45)
    if img_response.status_code == 200 and len(img_response.content) > 1000:
        raw_img = Image.open(BytesIO(img_response.content)).convert("RGBA")
        # قص 40 بكسل من كل جهة لإزالة العلامة المائية في الأسفل
        bg_image = raw_img.crop((40, 40, 1120, 1120)).resize((1080, 1080))
        print("✅ تم توليد الخلفية وإزالة العلامة المائية بنجاح!")
except Exception as e:
    print(f"⚠️ تعذر جلب الصورة الخارجية: {e}")

if bg_image is None:
    bg_image = Image.new("RGBA", (1080, 1080), (10, 18, 36, 255))

# طبقة تظليل فخمة لإبراز النص العربي بوضوح عالٍ
overlay = Image.new("RGBA", (1080, 1080), (6, 12, 26, 195))
final_img = Image.alpha_composite(bg_image, overlay).convert("RGB")
draw = ImageDraw.Draw(final_img)

# 3. تحميل خط عربي أصلي (Tajawal Bold) يدعم الربط الكامل
print("3. جاري تحميل الخط العربي وتصميم البطاقة...")
font_url = "https://github.com/google/fonts/raw/main/ofl/tajawal/Tajawal-Bold.ttf"
font_bytes = requests.get(font_url, timeout=20).content

title_font = ImageFont.truetype(BytesIO(font_bytes), 64, layout_engine=ImageFont.Layout.RAQM)
brand_font = ImageFont.truetype(BytesIO(font_bytes), 42, layout_engine=ImageFont.Layout.RAQM)
footer_font = ImageFont.truetype(BytesIO(font_bytes), 30, layout_engine=ImageFont.Layout.RAQM)

# 4. رسم الإطار والهوية البصرية (مداميك | MdaMiak)
draw.rectangle([(55, 55), (1025, 1025)], outline=(0, 210, 255), width=2)
draw.text((540, 130), "MdaMiak | مداميك", font=brand_font, fill=(0, 210, 255), anchor="mm", direction="rtl")
draw.line([(380, 175), (700, 175)], fill=(0, 210, 255), width=3)

# 5. تقسيم وطباعة العنوان الرئيسي في المنتصف باتجاه عربي سليم (RTL)
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
    y_pos += 100

# 6. طباعة التوقيع السفلي
draw.text((540, 955), "نبني مستقبلك الرقمي بذكاء | @MdaMiak", font=footer_font, fill=(180, 200, 225), anchor="mm", direction="rtl")

# 7. حفظ المخرجات
os.makedirs("output", exist_ok=True)
final_img.save("output/post_image.jpg", quality=95)
with open("output/caption.txt", "w", encoding="utf-8") as f:
    f.write(caption)

print("🎉 تم إنتاج التصميم الجديد بنجاح!")
