import os
import json
import time
import requests
from playwright.sync_api import sync_playwright

# ==========================================
# 1. توليد البطاقة البصرية الاحترافية
# ==========================================
def generate_perfect_card(title, body_points, output_path="output.png"):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }}
            body {{
                width: 1080px; height: 1080px; background-color: #0b1329;
                background-image: radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
                                  radial-gradient(at 0% 100%, rgba(37, 99, 235, 0.2) 0px, transparent 50%);
                color: #ffffff; display: flex; align-items: center; justify-content: center; padding: 40px;
            }}
            .card {{
                width: 100%; height: 100%; border: 2px solid rgba(56, 189, 248, 0.3);
                border-radius: 28px; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px);
                padding: 50px 60px; display: flex; flex-direction: column; justify-content: space-between;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }}
            .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(51, 65, 85, 0.8); padding-bottom: 24px; }}
            .brand-ar {{ font-size: 40px; font-weight: 900; color: #38bdf8; }}
            .brand-en {{ font-size: 26px; font-weight: 700; color: #94a3b8; letter-spacing: 1px; }}
            .main-content {{ display: flex; flex-direction: column; gap: 30px; text-align: center; margin: auto 0; }}
            .title {{ font-size: 46px; font-weight: 900; line-height: 1.4; color: #ffffff; }}
            .content-box {{ background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 35px 30px; display: flex; flex-direction: column; gap: 18px; }}
            .point {{ font-size: 28px; font-weight: 600; color: #cbd5e1; }}
            .highlight {{ color: #38bdf8; font-weight: 700; }}
            .footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 2px solid rgba(51, 65, 85, 0.8); padding-top: 24px; font-size: 22px; font-weight: 600; color: #94a3b8; }}
            .website {{ color: #38bdf8; direction: ltr; }}
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
    print("🎨 تم توليد الصورة الاحترافية بنجاح.")

# ==========================================
# 2. النشر التلقائي عبر متصفح سحابي
# ==========================================
def publish_via_meta_business(cookies_json, image_path, caption):
    """أتمتة النشر المباشر على صفحة فيسبوك وانستغرام دون استخدام أي API أو توكنات"""
    print("🌐 جارٍ تشغيل المتصفح والدخول إلى Meta Business Suite...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        # تحميل الجلسة المسجلة
        try:
            cookies = json.loads(cookies_json)
            # ضبط صيغة الكوكيز لتقبلها Playwright
            for cookie in cookies:
                if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                    del cookie["sameSite"]
            context.add_cookies(cookies)
        except Exception as e:
            print(f"❌ خطأ في تحميل الكوكيز: {e}")
            browser.close()
            return False

        page = context.new_page()
        page.goto("https://business.facebook.com/latest/composer", wait_until="networkidle")
        time.sleep(5)

        # التحقق من صفحة النشر
        if "login" in page.url:
            print("❌ انتهت صلاحية جلسة المتصفح أو لم يتم العثور على تسجيل الدخول. يرجى تجديد الكوكيز.")
            browser.close()
            return False

        try:
            print("📝 جارٍ رفع الصورة وإضافة المحتوى التسويقي...")
            # 1. رفع الصورة
            file_input = page.locator('input[type="file"]')
            file_input.set_input_files(os.path.abspath(image_path))
            time.sleep(4)

            # 2. كتابة النص
            text_area = page.locator('div[role="textbox"]').first
            text_area.click()
            page.keyboard.type(caption, delay=20)
            time.sleep(3)

            # 3. الضغط على زر النشر
            publish_btn = page.locator('button:has-text("نشر"), button:has-text("Publish")').first
            publish_btn.click()
            print("🚀 تم الضغط على زر النشر بنجاح! جارٍ الانتظار لاكتمال المعالجة...")
            time.sleep(8)
            print("✅ تم النشر بنجاح على فيسبوك وإنستغرام عبر المتصفح المباشر!")
            browser.close()
            return True

        except Exception as e:
            print(f"❌ تعذر إتمام النشر عبر واجهة المتصفح: {e}")
            page.screenshot(path="debug_error.png")
            browser.close()
            return False

def send_to_telegram(bot_token, chat_id, image_path, caption):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(image_path, "rb") as img_file:
        data = {"chat_id": chat_id, "caption": caption}
        files = {"photo": img_file}
        requests.post(url, data=data, files=files)
    print("📲 تم إرسال المعاينة إلى تيليجرام.")

# ==========================================
# 3. نقطة التشغيل الرئيسية
# ==========================================
def main():
    fb_cookies = os.getenv("FB_COOKIES_JSON")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    image_path = "output.png"
    
    title = "أتمتة العمليات الرقمية لشركتك"
    points = [
        "حوّل مهامك الروتينية المتكررة إلى تدفقات ذكية",
        "ارفع كفاءة التشغيل وخفّض الهدر الزمني بنسبة 40%",
        "وكلاء ذكاء اصطناعي مخصصون لتطوير أعمالك"
    ]

    # توليد البطاقة
    generate_perfect_card(title, points, image_path)

    post_caption = """كفاءة أعلى، وقت أسرع، وأخطاء أقل.

في مِداميك نطور لك وكلاء ذكاء اصطناعي مخصصين لأتمتة أعمالك ورفع الكفاءة التشغيلية.

#مِداميك #MdaMiak #أتمتة_الأعمال #ذكاء_اصطناعي #تحول_رقمي"""

    # تنفيذ النشر المباشر عبر المتصفح
    if fb_cookies:
        publish_via_meta_business(fb_cookies, image_path, post_caption)
    else:
        print("⚠️ لم يتم العثور على FB_COOKIES_JSON في Secrets.")

    # إرسال المعاينة لتيليجرام
    if tg_token and tg_chat_id:
        send_to_telegram(tg_token, tg_chat_id, image_path, post_caption)

if __name__ == "__main__":
    main()
