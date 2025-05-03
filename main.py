from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from analyzer import analyze_log

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, log: str = Form(...)):
    result = analyze_log(log)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "analysis": result["analysis"],
        "fix": result["fix"],
        "log": log
    })
