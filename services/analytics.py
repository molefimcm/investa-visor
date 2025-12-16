from db import get_db

def user_analytics(user_id: int) -> dict:
    db = get_db()

    total_plans = db.execute(
        "SELECT COUNT(*) AS c FROM plans WHERE user_id = ?",
        (user_id,)
    ).fetchone()["c"]

    plans_by_type = db.execute(
        """
        SELECT plan_type, COUNT(*) AS c
        FROM plans
        WHERE user_id = ?
        GROUP BY plan_type
        ORDER BY c DESC
        """,
        (user_id,)
    ).fetchall()

    recent_plans = db.execute(
        """
        SELECT id, plan_type, created_at
        FROM plans
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 10
        """,
        (user_id,)
    ).fetchall()

    events_by_type = db.execute(
        """
        SELECT event_type, COUNT(*) AS c
        FROM events
        WHERE user_id = ?
        GROUP BY event_type
        ORDER BY c DESC
        """,
        (user_id,)
    ).fetchall()

    return {
        "total_plans": total_plans,
        "plans_by_type": [dict(r) for r in plans_by_type],
        "recent_plans": [dict(r) for r in recent_plans],
        "events_by_type": [dict(r) for r in events_by_type],
    }
