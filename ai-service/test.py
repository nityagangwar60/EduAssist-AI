from google import genai
from config import GEMINI_API_KEY

print("Loaded key:", repr(GEMINI_API_KEY))
print("Starts with:", GEMINI_API_KEY[:10] if GEMINI_API_KEY else "None")

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say Hello"
)

print(response.text)