import os
import json
import urllib.parse
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from google import genai

# 1. إعداد الاتصال بـ Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

prompt = """
أنت المدير الإبداعي لعلامة (مَداميك | MdaMiak) المتخصصة في الأتمتة، وكلاء الذكاء الاصطناعي، والحلول الرقمية للأعمال.
ابتكر منشوراً احترافياً وجذاباً لفيسبوك وانستجرام يقدم فائدة عملية أو أداة ذكية أو فكرة أتمتة تزيد الإنتاجية.
أخرج النتيجة بصيغة JSON فقط بدون أي نص إضافي أو علامات، تحتوي على المفاتيح التالية:
{
  "headline": "عنوان عربي خاطف للانتباه للتصميم (من 5 إلى 8 كلمات كحد أقصى)",
  "caption": "نص المنشور الكامل بأسلوب شيق واحترافي مع نقاط واضحة وسؤال تفاعلي في النهاية والهاشتاجات المناسبة",
  "image_prompt": "Detailed English prompt for a futuristic, sleek, dark-mode minimalist 3D tech background representing AI automation and digital building blocks, luxury dark navy blue and glowing cyan/gold accents, no text, 8k"
}
"""

print("1. جاري توليد فكرة ونص المنشور عبر Gemini...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={"response_mime_type": "application/json"}
)

data = json.loads(response.text)
headline = data["headline"]
caption = data["caption"]
image_prompt = data["image_prompt"]

print(f"العنوان المختار: {headline}")

# 2. توليد الخلفية البصرية مجاناً عبر Pollinations (Flux)
print("2. جاري توليد الخلفية البصرية...")
encoded_prompt = urllib.parse.quote(image_prompt)
image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1080&nologo=true&seed=42"

img_response = requests.get(image_url, timeout=60)
bg_image = Image.open(BytesIO(img_response.content)).convert("RGBA")
bg_image = bg_image.resize((1080, 1080))

# إضافة طبقة تظليل داكنة أنيقة لإبراز النص العربي
overlay = Image.new("RGBA", (1080, 1080), (10, 18, 35, 185))
final_img = Image.alpha_composite(bg_image, overlay).convert("RGB")
draw = ImageDraw.Draw(final_img)

# 3. تحميل خط عربي احترافي (Cairo Bold) تلقائياً
font_url = "https://github.com/google/fonts/raw/main/ofl/cairo/static/Cairo-Bold.ttf"
font_bytes = requests.get(font_url).content

title_font = ImageFont.truetype(BytesIO(font_bytes), 62)
brand_font = ImageFont.truetype(BytesIO(font_bytes), 38)
footer_font = ImageFont.truetype(BytesIO(font_bytes), 30)

def shape_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# 4. طباعة الهوية البصرية (مَداميك | MdaMiak) في الأعلى
brand_text = shape_arabic("مَداميك | MdaMiak")
draw.text((540, 110), brand_text, font=brand_font, fill=(0, 210, 255), anchor="mm")
draw.line([(390, 155), (690, 155)], fill=(0, 210, 255), width=3)

# 5. تقسيم وطباعة العنوان الرئيسي في المنتصف
words = headline.split()
lines = []
current_line = []
for word in words:
    current_line.append(word)
    if len(current_line) >= 4:
        lines.append(" ".join(current_line))
        current_line = []
if current_line:
    lines.append(" ".join(current_line))

y_pos = 480 - (len(lines) * 45)
for line in lines:
    shaped_line = shape_arabic(line)
    draw.text((540, y_pos), shaped_line, font=title_font, fill=(255, 255, 255), anchor="mm")
    y_pos += 100

# 6. طباعة التوقيع السفلي
footer_text = shape_arabic("نبني مستقبلك الرقمي بذكاء | @MdaMiak")
draw.text((540, 970), footer_text, font=footer_font, fill=(190, 200, 220), anchor="mm")

# 7. حفظ المخرجات (الصورة + نص المنشور)
os.makedirs("output", exist_ok=True)
final_img.save("output/post_image.jpg", quality=95)
with open("output/caption.txt", "w", encoding="utf-8") as f:
    f.write(caption)

print("تم تصميم البطاقة وكتابة المنشور بنجاح داخل مجلد output!")
