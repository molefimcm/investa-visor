from db import get_db

def upsert_profile(user_id: int, monthly: float, risk: str, horizon: str, markets: str, experience: str):
    db = get_db()
    existing = db.execute(
        "SELECT user_id FROM user_investment_profiles WHERE user_id=?",
        (user_id,),
    ).fetchone()

    if existing:
        db.execute(
            """UPDATE user_investment_profiles
               SET monthly_invest_amount=?, risk_appetite=?, time_horizon=?, markets=?, experience_level=?
               WHERE user_id=?""",
            (monthly, risk, horizon, markets, experience, user_id),
        )
    else:
        db.execute(
            """INSERT INTO user_investment_profiles
               (user_id, monthly_invest_amount, risk_appetite, time_horizon, markets, experience_level)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, monthly, risk, horizon, markets, experience),
        )
    db.commit()

def get_profile(user_id: int):
    db = get_db()
    return db.execute(
        "SELECT * FROM user_investment_profiles WHERE user_id=?",
        (user_id,),
    ).fetchone()
