from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI()

# ربط ملفات CSS وJS
app.mount("/static", StaticFiles(directory="static"), name="static")

# قوالب HTML
templates = Jinja2Templates(directory="templates")

# قائمة لتخزين البريد مؤقتاً (يمكن استبدالها بقاعدة بيانات)
subscribers = []

# الصفحة الرئيسية
@app.get("/")
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# نموذج الاشتراك
@app.post("/subscribe")
async def subscribe(request: Request, email: str = Form(...)):
    subscribers.append(email)  # تخزين البريد مؤقتاً
    # لاحقاً يمكن ربطه بـ Google Sheets أو MailChimp
    return templates.TemplateResponse("thankyou.html", {"request": request, "email": email})

# دالة main لتشغيل السيرفر مباشرة
def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# تنفيذ دالة main إذا شغلت الملف مباشرة
if __name__ == "__main__":
    main()
