from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import analyzer

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_log(request: Request, log: str = Form(...)):
    result = analyzer.analyze_log_with_model(log)
    if isinstance(result, dict):
        analysis = result.get("analysis", "No analysis.")
        fix = result.get("fix", "No fix.")
    else:
        analysis = fix = "Invalid response from model."
    return templates.TemplateResponse("index.html", {
        "request": request,
        "analysis": analysis,
        "fix": fix
    })
