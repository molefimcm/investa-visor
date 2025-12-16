from config import DISCLAIMER_TEXT

def call_llm(system_prompt: str, user_prompt: str) -> str:
    return (
        "InvestaVisor Daily Plan\n\n"
        f"{user_prompt}\n\n"
        "Reminder\n"
        "- This guidance is based on your stated profile and long-term discipline.\n"
        "- No stock picks. No predictions. No trading.\n\n"
        f"Disclaimer: {DISCLAIMER_TEXT}"
    )
