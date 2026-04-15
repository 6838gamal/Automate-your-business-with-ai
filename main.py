from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# ملفات CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# قائمة بريد مؤقتة
subscribers = []

@app.get("/")
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/subscribe")
async def subscribe(request: Request, email: str = Form(...)):
    subscribers.append(email)
    return templates.TemplateResponse("thankyou.html", {"request": request, "email": email})

def main():
    uvicorn.run("main:app", port=8000, reload=False)

if __name__ == "__main__":
    main()
