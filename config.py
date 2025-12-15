import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DATABASE = os.getenv("DATABASE", "investa.db")

# MVP: no GPT costs
USE_LLM = False

DISCLAIMER_TEXT = (
    "InvestaVisor is an educational research utility and personal discipline assistant. "
    "It is NOT a licensed financial advisor and does NOT provide personalized investment, "
    "legal, tax, or financial advice. Use it for initial research support and routines only. "
    "Always do your own research and consult a qualified professional before making decisions."
)
