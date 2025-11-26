# find_working_model.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("No GEMINI_API_KEY in .env")

client = genai.Client(api_key=API_KEY)

candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-mini",
    "gemini-2.1",
    "gemini-2.1-flash",
    "gemini-1.0",
    "gemini-proto-1",
]

for model in candidates:
    try:
        print("Trying model:", model)
        resp = client.models.generate_content(model=model, contents="Hello. Say one short sentence.")
        text = getattr(resp, "text", None) or str(resp)
        print("SUCCESS with", model, "→ preview:", text[:200])
        break
    except Exception as e:
        print("Failed:", model, "->", e)
else:
    print("None of the candidate models worked. Run list_models.py and paste the output.")
