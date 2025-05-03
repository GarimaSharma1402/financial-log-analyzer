import requests

GROQ_API_KEY = "groq_api_key"  # Set in Render as an env variable
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def analyze_log(log: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a financial log analysis assistant.

Log: {log}

Provide:
1. A brief analysis of the log in simple English.
2. A suggested fix or explanation for the issue.
"""

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        data = response.json()
        content = data['choices'][0]['message']['content']

        analysis, fix = content.split("Fix:", 1) if "Fix:" in content else (content, "No fix provided.")

        return {
            "analysis": analysis.strip(),
            "fix": fix.strip()
        }
    except Exception as e:
        return {
            "analysis": "Error analyzing log.",
            "fix": str(e)
        }
