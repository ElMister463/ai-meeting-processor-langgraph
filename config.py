import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
TOKEN_PATH = os.getenv("TOKEN_PATH")

if not OPENAI_API_KEY:
    raise ValueError("No se encontró OPENAI_API_KEY en el entorno")
