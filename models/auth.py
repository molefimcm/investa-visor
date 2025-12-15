from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

def create_user(email: str, password: str) -> int:
    db = get_db()
    pw_hash = generate_password_hash(password)
    db.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email.strip().lower(), pw_hash),
    )
    db.commit()
    row = db.execute("SELECT id FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    return row["id"]

def get_user_by_email(email: str):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.strip().lower(),),
    ).fetchone()

def verify_password(user_row, password: str) -> bool:
    return check_password_hash(user_row["password_hash"], password)
