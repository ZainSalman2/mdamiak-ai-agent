import os
import sys
import json
import urllib.parse
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from google import genai

# 1. فحص مفتاح Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("❌ خطأ: لم يتم العثور على مفتاح GEMINI_API_KEY في GitHub Secrets!")
    sys.exit(1)

client = genai.Client(api_key=api_key.strip())

prompt = """
أنت المدير الإبداعي لعلامة (مَداميك | MdaMiak) المتخصصة في الأتمتة، وكلاء الذكاء الاصطناعي، والحلول الرقمية للأعمال.
ابتكر منشوراً احترافياً وجذاباً لفيسبوك وانستجرام يقدم فائدة عملية أو أداة ذكية أو فكرة أتمتة تزيد الإنتاجية.
أخرج النتيجة بصيغة JSON فقط تحتوي على المفاتيح التالية:
{
  "headline": "عنوان عربي خاطف للانتباه للتصميم من 4 إلى 7 كلمات",
  "caption": "نص المنشور الكامل بأسلوب شيق واحترافي مع نقاط واضحة وسؤال تفاعلي في النهاية والهاشتاجات المناسبة",
  "image_prompt": "Futuristic sleek dark-mode minimalist 3D tech background representing AI automation and digital building blocks, luxury dark navy blue and glowing cyan accents, abstract geometry, no text, 8k"
}
"""

print("1. جاري توليد فكرة ونص المنشور عبر Gemini...")
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    data = json.loads(raw_text)
except Exception as e:
    print(f"⚠️ تنبيه في استجابة Gemini، سيتم استخدام محتوى احتياطي: {e}")
    data = {
        "headline": "كيف تضاعف إنتاجية عملك بالذكاء الاصطناعي؟",
        "caption": "في مَداميك | MdaMiak نبني لك أنظمة ذكية تعمل نيابة عنك على مدار الساعة.\n\nما هي المهمة اليومية التي تتمنى أتمتتها في عملك؟ شاركنا في التعليقات! 👇\n\n#مداميك #MdaMiak #ذكاء_اصطناعي #أتمتة",
        "image_prompt": "Futuristic dark navy blue 3D tech background glowing cyan nodes"
    }

headline = data.get("headline", "حلول الأتمتة الذكية من مَداميك")
caption = data.get("caption", "")
image_prompt = data.get("image_prompt", "Futuristic dark tech background")
print(f"✅ العنوان المختار: {headline}")

# 2. توليد الخلفية البصرية (مع نظام بديل تلقائي إذا تأخر السيرفر)
print("2. جاري تجهيز الخلفية البصرية...")
bg_image = None
try:
    encoded_prompt = urllib.parse.quote(image_prompt)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true&seed=101"
    headers = {"User-Agent": "Mozilla/5.0"}
    img_response = requests.get(image_url, headers=headers, timeout=45)
    if img_response.status_code == 200 and len(img_response.content) > 1000:
        bg_image = Image.open(BytesIO(img_response.content)).convert("RGBA").resize((1080, 1080))
        print("✅ تم توليد الخلفية بالذكاء الاصطناعي بنجاح!")
except Exception as e:
    print(f"⚠️ تعذر جلب الصورة الخارجية، جاري إنشاء خلفية هندسية بديلة: {e}")

if bg_image is None:
    bg_image = Image.new("RGBA", (1080, 1080), (12, 22, 44, 255))

# إضافة طبقة تظليل داكنة أنيقة لإبراز النص العربي
overlay = Image.new("RGBA", (1080, 1080), (8, 15, 30, 190))
final_img = Image.alpha_composite(bg_image, overlay).convert("RGB")
draw = ImageDraw.Draw(final_img)

# 3. تحميل خط عربي احترافي (مع روابط متعددة لضمان التحميل)
print("3. جاري تحميل الخط العربي وتصميم البطاقة...")
font_urls = [
    "https://raw.githubusercontent.com/googlefonts/cairo/main/fonts/ttf/Cairo-Bold.ttf",
    "https://raw.githubusercontent.com/google/fonts/main/ofl/tajawal/Tajawal-Bold.ttf"
]

font_bytes = None
for url in font_urls:
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            font_bytes = r.content
            break
    except Exception:
        continue

if font_bytes:
    title_font = ImageFont.truetype(BytesIO(font_bytes), 60)
    brand_font = ImageFont.truetype(BytesIO(font_bytes), 38)
    footer_font = ImageFont.truetype(BytesIO(font_bytes), 28)
else:
    title_font = ImageFont.load_default()
    brand_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

def shape_arabic(text):
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text

# 4. طباعة إطار وهوية (مَداميك | MdaMiak)
draw.rectangle([(60, 60), (1020, 1020)], outline=(0, 210, 255), width=2)
brand_text = shape_arabic("مَداميك | MdaMiak")
draw.text((540, 130), brand_text, font=brand_font, fill=(0, 210, 255), anchor="mm")
draw.line([(380, 175), (700, 175)], fill=(0, 210, 255), width=3)

# 5. تقسيم وطباعة العنوان الرئيسي في المنتصف
words = headline.split()
lines, current_line = [], []
for word in words:
    current_line.append(word)
    if len(current_line) >= 4:
        lines.append(" ".join(current_line))
        current_line = []
if current_line:
    lines.append(" ".join(current_line))

y_pos = 500 - (len(lines) * 45)
for line in lines:
    shaped_line = shape_arabic(line)
    draw.text((540, y_pos), shaped_line, font=title_font, fill=(255, 255, 255), anchor="mm")
    y_pos += 95

# 6. طباعة التوقيع السفلي
footer_text = shape_arabic("نبني مستقبلك الرقمي بذكاء | @MdaMiak")
draw.text((540, 950), footer_text, font=footer_font, fill=(180, 195, 215), anchor="mm")

# 7. حفظ المخرجات
os.makedirs("output", exist_ok=True)
final_img.save("output/post_image.jpg", quality=95)
with open("output/caption.txt", "w", encoding="utf-8") as f:
    f.write(caption)

print("🎉 تم تصميم البطاقة وكتابة المنشور بنجاح داخل مجلد output!")
