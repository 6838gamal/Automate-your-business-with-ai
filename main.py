from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import sqlite3
import re

app = FastAPI()

# ملفات static
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# قاعدة بيانات
conn = sqlite3.connect("subscribers.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE
)
""")
conn.commit()

# تحقق من الإيميل
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# الصفحة الرئيسية
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )

# الاشتراك
@app.post("/subscribe")
async def subscribe(request: Request, email: str = Form(...)):

    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email")

    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
    except sqlite3.IntegrityError:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": "هذا البريد مسجل مسبقًا"
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="thankyou.html",
        context={
            "request": request,
            "email": email
        }
    )

# عرض المشتركين (API بسيط)
@app.get("/subscribers")
async def get_subscribers():
    cursor.execute("SELECT email FROM subscribers")
    data = cursor.fetchall()
    return {"subscribers": [row[0] for row in data]}

# تشغيل السيرفر
def main():
    uvicorn.run("main:app", port=8000, reload=False)

if __name__ == "__main__":
    main()
