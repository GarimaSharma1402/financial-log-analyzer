from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_log_with_model

app = FastAPI()

class LogRequest(BaseModel):
    log: str

@app.post("/analyze")
async def analyze_log(request: LogRequest):
    # Call the function to analyze the log using the Groq API
    result = analyze_log_with_model(request.log)
    
    # Return the result as a JSON response
    return result
