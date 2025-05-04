import os
import requests
import json
import html

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

def analyze_log_with_model(log: str):
    if not log.strip():
        return {"analysis": "Empty log input.", "fix": "Please enter a valid log message."}

    # Escape HTML-sensitive characters to reduce risk of injection issues in the prompt
    sanitized_log = html.escape(log)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a helpful assistant specialized in financial systems error analysis.

Analyze the following financial log and respond in JSON format with "analysis" and "fix".

Log: {sanitized_log}

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

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    except Exception as req_err:
        return {"analysis": "Request failed.", "fix": str(req_err)}

    if response.status_code == 200:
        try:
            raw_output = response.json()["choices"][0]["message"]["content"]
            # Try parsing structured response
            return json.loads(raw_output)
        except json.JSONDecodeError:
            return {
                "analysis": "Could not parse model response.",
                "fix": "Try simplifying the log input. Avoid emojis, code snippets, or overly long/symbol-heavy messages."
            }
        except Exception as e:
            return {"analysis": "Unknown error parsing model response.", "fix": str(e)}
    else:
        return {"analysis": "API call failed.", "fix": f"Status: {response.status_code}, Error: {response.text}"}
