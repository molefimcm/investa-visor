from db import get_db

def upsert_personal(user_id: int, first_name: str, last_name: str, country=None, timezone=None):
    db = get_db()
    existing = db.execute(
        "SELECT user_id FROM user_personal_details WHERE user_id=?",
        (user_id,),
    ).fetchone()

    if existing:
        db.execute(
            """UPDATE user_personal_details
               SET first_name=?, last_name=?, country=?, timezone=?
               WHERE user_id=?""",
            (first_name, last_name, country, timezone, user_id),
        )
    else:
        db.execute(
            """INSERT INTO user_personal_details (user_id, first_name, last_name, country, timezone)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, first_name, last_name, country, timezone),
        )
    db.commit()

def get_personal(user_id: int):
    db = get_db()
    return db.execute(
        "SELECT * FROM user_personal_details WHERE user_id=?",
        (user_id,),
    ).fetchone()
