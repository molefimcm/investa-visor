import json
from db import get_db

def log_event(user_id, event_type: str, payload=None):
    db = get_db()
    db.execute(
        "INSERT INTO events (user_id, event_type, event_payload) VALUES (?, ?, ?)",
        (user_id, event_type, json.dumps(payload) if payload else None),
    )
    db.commit()
