from config import USE_LLM, DISCLAIMER_TEXT

def call_llm(system_prompt: str, user_prompt: str) -> str:
    # MVP: no costs, no external calls
    return (
        "InvestaVisor Daily Plan (MVP)\n\n"
        "Today's Focus\n"
        "- Stay consistent: follow your monthly contribution plan.\n"
        "- Avoid emotional decisions: no impulse buys/sells today.\n\n"
        "Suggested Actions\n"
        "- Check your holdings briefly (5–10 minutes max).\n"
        "- Note any big changes in price/earnings/news to research later.\n"
        "- If you're investing monthly, schedule your next contribution.\n\n"
        "Risk & Discipline Reminder\n"
        "- Don’t chase hype. Don’t panic sell. Zoom out to your time horizon.\n\n"
        "Today's Lesson\n"
        "- The investor’s edge is discipline. Simple routines beat complex strategies.\n\n"
        f"Disclaimer: {DISCLAIMER_TEXT}"
    )
