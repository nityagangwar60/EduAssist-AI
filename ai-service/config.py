import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

print("API KEY =", OPENROUTER_API_KEY)

MODEL = os.getenv(
    "MODEL",
    "nvidia/nemotron-nano-9b-v2:free"
)