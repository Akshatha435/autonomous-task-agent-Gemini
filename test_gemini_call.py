# test_gemini_call.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
print("API_KEY prefix:", API_KEY[:4] if API_KEY else None)

client = genai.Client(api_key=API_KEY)
resp = client.models.generate_content(model="gemini-1.5-mini", contents="Say hello in one sentence.")
print("Response preview:", getattr(resp, "text", str(resp))[:200])
