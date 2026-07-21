import requests

from config import OPENROUTER_API_KEY, MODEL

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(question, context="", memory=""):
    prompt = f"""
You are EduAssist AI.

Previous Conversation:
{memory}

Knowledge Base:
{context}

Current Question:
{question}

Instructions:
- Use previous conversation if relevant.
- Use the knowledge base.
- If the answer is not found, politely say it is unavailable.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    print("MODEL =", MODEL)
    print("URL =", URL)

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.3,
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=60)
        data = response.json()

        print("OPENROUTER RESPONSE:")
        print(data)

        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return "AI response error: " + str(data)
    except Exception as e:
        return str(e)