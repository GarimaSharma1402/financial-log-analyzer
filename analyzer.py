import os
import requests
import json  # ✅ Needed for parsing the model's JSON string

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

def analyze_log_with_model(log: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a helpful assistant specialized in financial systems error analysis.

Analyze the following financial log and respond in JSON format with "analysis" and "fix".

Log: {log}

Respond like:
{{
  "analysis": "...",
  "fix": "..."
}}
"""

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a financial systems expert."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        try:
            raw_output = response.json()["choices"][0]["message"]["content"]
            return json.loads(raw_output)  # ✅ Convert JSON string to Python dict
        except Exception as e:
            return {"analysis": "Could not parse model response.", "fix": str(e)}
    else:
        return {"analysis": "API call failed.", "fix": f"Status: {response.status_code}, Error: {response.text}"}
