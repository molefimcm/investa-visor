from db import get_db

def save_plan(user_id: int, plan_type: str, input_context: str, response_text: str):
    db = get_db()
    db.execute(
        "INSERT INTO plans (user_id, plan_type, input_context, response_text) VALUES (?, ?, ?, ?)",
        (user_id, plan_type, input_context, response_text),
    )
    db.commit()

def list_plans(user_id: int, limit: int = 20):
    db = get_db()
    return db.execute(
        "SELECT id, plan_type, input_context, created_at FROM plans WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()

def get_plan(user_id: int, plan_id: int):
    db = get_db()
    return db.execute(
        "SELECT * FROM plans WHERE user_id=? AND id=?",
        (user_id, plan_id),
    ).fetchone()
