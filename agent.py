import os
import requests
from playwright.sync_api import sync_playwright

# ==========================================
# 1. محرك التصميم فائق الدقة (HTML/CSS Browser)
# ==========================================
def generate_perfect_card(title, body_points, output_path="output.png"):
    """توليد بطاقة تسويقية بدقة 1080x1080 عبر محرك Chromium لضمان سلامة الخط العربي 100%"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Cairo', sans-serif;
            }}
            body {{
                width: 1080px;
                height: 1080px;
                background-color: #0b1329;
                background-image: 
                    radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                    radial-gradient(at 0% 100%, rgba(37, 99, 235, 0.2) 0px, transparent 50%);
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 40px;
            }}
            .card {{
                width: 100%;
                height: 100%;
                border: 2px solid rgba(56, 189, 248, 0.3);
                border-radius: 28px;
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(12px);
                padding: 50px 60px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid rgba(51, 65, 85, 0.8);
                padding-bottom: 24px;
            }}
            .brand-ar {{
                font-size: 40px;
                font-weight: 900;
                color: #38bdf8;
            }}
            .brand-en {{
                font-size: 26px;
                font-weight: 700;
                color: #94a3b8;
                letter-spacing: 1px;
            }}
            .main-content {{
                display: flex;
                flex-direction: column;
                gap: 30px;
                text-align: center;
                margin: auto 0;
            }}
            .title {{
                font-size: 46px;
                font-weight: 900;
                line-height: 1.4;
                color: #ffffff;
            }}
            .content-box {{
                background: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-radius: 20px;
                padding: 35px 30px;
                display: flex;
                flex-direction: column;
                gap: 18px;
            }}
            .point {{
                font-size: 28px;
                font-weight: 600;
                color: #cbd5e1;
            }}
            .highlight {{
                color: #38bdf8;
                font-weight: 700;
            }}
            .footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 2px solid rgba(51, 65, 85, 0.8);
                padding-top: 24px;
                font-size: 22px;
                font-weight: 600;
                color: #94a3b8;
            }}
            .website {{
                color: #38bdf8;
                direction: ltr;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="brand-ar">مِداميك للذكاء الاصطناعي</div>
                <div class="brand-en">MdaMiak AI</div>
            </div>
            
            <div class="main-content">
                <div class="title">{title}</div>
                <div class="content-box">
                    <div class="point">{body_points[0]}</div>
                    <div class="point highlight">{body_points[1]}</div>
                    <div class="point">{body_points[2]}</div>
                </div>
            </div>

            <div class="footer">
                <div>نحو تحول رقمي متكامل بحلول الأتمتة والذكاء الاصطناعي</div>
                <div class="website">mdamiak.com</div>
            </div>
        </div>
    </body>
    </html>
    """

    with open("card_template.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        page.goto(f"file://{os.path.abspath('card_template.html')}")
        page.wait_for_load_state("networkidle")
        page.screenshot(path=output_path)
        browser.close()
    
    print("🎨 تم توليد الصورة الاحترافية بنجاح عبر المحرك البصري.")

# ==========================================
# 2. دوال النشر والإرسال
# ==========================================
def post_to_facebook(page_id, access_token, image_path, caption):
    url = f"https://graph.facebook.com/v26.0/{page_id}/photos"
    with open(image_path, "rb") as img_file:
        payload = {"caption": caption, "access_token": access_token}
        files = {"source": img_file}
        response = requests.post(url, data=payload, files=files)
    
    res = response.json()
    if response.status_code == 200 and "id" in res:
        print(f"✅ تم النشر بنجاح على فيسبوك! معرف المنشور: {res['id']}")
        return True
    else:
        err = res.get('error', {})
        print(f"❌ خطأ صريح من فيسبوك: [{err.get('code')}] {err.get('message')}")
        return False

def send_to_telegram(bot_token, chat_id, image_path, caption):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(image_path, "rb") as img_file:
        data = {"chat_id": chat_id, "caption": caption}
        files = {"photo": img_file}
        res = requests.post(url, data=data, files=files)
    if res.status_code == 200:
        print("✅ تم إرسال البطاقة لمعاينتها على تيليجرام.")

# ==========================================
# 3. التشغيل
# ==========================================
def main():
    fb_page_id = os.getenv("FB_PAGE_ID")
    fb_page_token = os.getenv("FB_PAGE_TOKEN")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    image_path = "output.png"
    
    # محتوى التصميم
    title = "أتمتة العمليات الرقمية لشركتك"
    points = [
        "حوّل مهامك الروتينية المتكررة إلى تدفقات ذكية",
        "ارفع كفاءة التشغيل وخفّض الهدر الزمني بنسبة 40%",
        "وكلاء ذكاء اصطناعي مخصصون لتطوير أعمالك"
    ]

    generate_perfect_card(title, points, image_path)

    post_caption = """كفاءة أعلى، وقت أسرع، وأخطاء أقل.

في مِداميك نطور لك وكلاء ذكاء اصطناعي مخصصين لأتمتة أعمالك ورفع الكفاءة التشغيلية.

#مِداميك #MdaMiak #أتمتة_الأعمال #ذكاء_اصطناعي #تحول_رقمي"""

    if fb_page_id and fb_page_token:
        print("🚀 جارٍ إرسال المنشور إلى فيسبوك...")
        post_to_facebook(fb_page_id, fb_page_token, image_path, post_caption)
    else:
        print("⚠️ مفاتيح فيسبوك غير متوفرة في Secrets.")

    if tg_token and tg_chat_id:
        send_to_telegram(tg_token, tg_chat_id, image_path, post_caption)

if __name__ == "__main__":
    main()
