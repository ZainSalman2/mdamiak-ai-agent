import os
import json
import random
import math
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# 1. الاتصال الذكي بـ Gemini API (يدعم gemini-3.8-flash ويكتشف النماذج تلقائياً)
api_key = os.environ.get("GEMINI_API_KEY", "").strip()

topics = [
    "3 أدوات ذكاء اصطناعي مجانية تضاعف إنتاجية رواد الأعمال",
    "كيف تربط واتساب بجدول بيانات جوجل للرد التلقائي على العملاء",
    "السر وراء كتابة أوامر (Prompts) احترافية تعطيك نتائج دقيقة من أول مرة",
    "كيف توفر 15 ساعة أسبوعياً عبر أتمتة المهام المتكررة في مشروعك",
    "لماذا تحتاج الشركات الناشئة إلى وكيل ذكاء اصطناعي (AI Agent)؟"
]
selected_topic = random.choice(topics)

prompt = f"""أنت المدير الإبداعي لعلامة (مَداميك | MdaMiak) المتخصصة في الأتمتة، وكلاء الذكاء الاصطناعي، والحلول الرقمية.
اكتب منشوراً احترافياً وجذاباً لفيسبوك وانستجرام حول: ({selected_topic}).
أرجع النتيجة بصيغة JSON فقط تحتوي على مفتاحين:
{{
  "headline": "عنوان عربي قوي وخاطف للانتباه بدون تشكيل من 5 إلى 7 كلمات",
  "caption": "نص المنشور الكامل بأسلوب شيق مع نقاط واضحة وسؤال تفاعلي في النهاية والهاشتاجات"
}}"""

print("1. جاري توليد المحتوى عبر Gemini...")
data = None
error_logs = []

# وضعنا gemini-3.8-flash في المقدمة + جلب تلقائي لأي نموذج متاح في الحساب
models = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.0-flash"]
try:
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    list_res = requests.get(list_url, timeout=10)
    if list_res.status_code == 200:
        for m in list_res.json().get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                m_name = m["name"].replace("models/", "")
                if m_name not in models:
                    models.append(m_name)
except Exception:
    pass

for model_name in models:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        res = requests.post(url, json=payload, timeout=20)
        if res.status_code == 200:
            raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            if "```" in raw_text:
                raw_text = raw_text.split("```")[1]
                if raw_text.lower().startswith("json"):
                    raw_text = raw_text[4:]
            start_idx = raw_text.find("{")
            end_idx = raw_text.rfind("}") + 1
            if start_idx != -1 and end_idx != 0:
                data = json.loads(raw_text[start_idx:end_idx])
                print(f"✅ نجح التوليد عبر نموذج: {model_name}")
                break
        else:
            error_logs.append(f"{model_name}: {res.status_code}")
    except Exception as e:
        error_logs.append(f"{model_name} Error: {str(e)}")

if not data:
    data = {
        "headline": "أتمتة المهام: سلاحك السري لمضاعفة أرباحك",
        "caption": "في مَداميك | MdaMiak نحول المهام اليومية المتكررة إلى أنظمة ذكية تعمل تلقائياً بدقة وسرعة.\n\n#مداميك #MdaMiak"
    }

headline = data.get("headline", "حلول الأتمتة الذكية من مداميك")
caption = data.get("caption", "")

# 2. رسم الخلفية التقنية الهندسية لعلامة MdaMiak
print("2. جاري تصميم البطاقة البصرية...")
W, H = 1080, 1080
base = Image.new("RGB", (W, H), (6, 11, 24))
draw_bg = ImageDraw.Draw(base)

cx, cy = W // 2, H // 2
for r in range(520, 0, -4):
    ratio = 1 - (r / 520)
    red = int(6 + 8 * ratio)
    green = int(14 + 65 * (ratio ** 1.5))
    blue = int(30 + 115 * (ratio ** 1.5))
    draw_bg.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(red, green, blue))

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_ov = ImageDraw.Draw(overlay)

for x in range(0, W, 90):
    draw_ov.line([(x, 0), (x, H)], fill=(0, 210, 255, 14), width=1)
for y in range(0, H, 90):
    draw_ov.line([(0, y), (W, y)], fill=(0, 210, 255, 14), width=1)

random.seed(len(headline) + random.randint(1, 10000))
nodes = [(random.randint(100, 980), random.randint(100, 980)) for _ in range(18)]
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        dist = math.hypot(nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1])
        if dist < 280:
            draw_ov.line([nodes[i], nodes[j]], fill=(0, 210, 255, 35), width=2)

for nx, ny in nodes:
    draw_ov.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=(0, 225, 255, 95))

final_img = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(final_img)

# 3. تحميل الخط العربي (Tajawal Bold)
font_url = "https://github.com/google/fonts/raw/main/ofl/tajawal/Tajawal-Bold.ttf"
font_bytes = requests.get(font_url, timeout=15).content

title_font = ImageFont.truetype(BytesIO(font_bytes), 64, layout_engine=ImageFont.Layout.RAQM)
brand_font = ImageFont.truetype(BytesIO(font_bytes), 42, layout_engine=ImageFont.Layout.RAQM)
footer_font = ImageFont.truetype(BytesIO(font_bytes), 30, layout_engine=ImageFont.Layout.RAQM)

# 4. رسم الإطار والهوية البصرية (مداميك | MdaMiak)
draw.rectangle([(50, 50), (1030, 1030)], outline=(0, 210, 255), width=2)
draw.rectangle([(62, 62), (1018, 1018)], outline=(0, 110, 160), width=1)

draw.text((540, 130), "مداميك | MdaMiak", font=brand_font, fill=(0, 215, 255), anchor="mm", direction="rtl")
draw.line([(370, 175), (710, 175)], fill=(0, 215, 255), width=3)

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
draw.line([(320, 910), (760, 910)], fill=(0, 110, 160), width=1)
draw.text((540, 955), "نبني مستقبلك الرقمي بذكاء | @MdaMiak", font=footer_font, fill=(185, 205, 230), anchor="mm", direction="rtl")

# 7. حفظ المخرجات
os.makedirs("output", exist_ok=True)
final_img.save("output/post_image.jpg", quality=95)
with open("output/caption.txt", "w", encoding="utf-8") as f:
    f.write(caption)

print("🎉 تم إنتاج التصميم والمنشور الجديد بنجاح!")
