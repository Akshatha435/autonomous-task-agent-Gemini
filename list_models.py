# list_models.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("No GEMINI_API_KEY in .env")

client = genai.Client(api_key=API_KEY)

print("Calling list models...")
try:
    resp = client.models.list()
    # print friendly summary
    for m in resp:
        try:
            name = getattr(m, "name", None) or (m.get("name") if isinstance(m, dict) else str(m))
        except Exception:
            name = str(m)
        print("-", name)
except Exception as e:
    print("ERROR listing models:", repr(e))
