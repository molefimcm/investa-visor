import os
import json
from flask import Flask, render_template, jsonify
from flask import request, session
from config import SECRET_KEY, DISCLAIMER_TEXT
from db import close_db, init_db
from models.auth import create_user, get_user_by_email, verify_password
from models.personal import upsert_personal, get_personal
from models.investment import upsert_profile, get_profile
from models.plans import save_plan, list_plans, get_plan
from services.events import log_event
from services.llm_client import call_llm
from services.advisor import classify_investor, allocation, principles
from functools import wraps


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.teardown_appcontext(close_db)

# Initializes DB: If DB or tables do not exist, create respectively based on the condition
def ensure_db():
    with app.app_context():
        init_db()

ensure_db()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper

@app.get("/")
def home():
    return render_template("index.html", disclaimer=DISCLAIMER_TEXT)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/auto-init")
def init_database():
    init_db()
    return jsonify({"status": "db initialized"})

@app.post("/api/signup")
def api_signup():
    data = request.get_json(force=True)
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    existing = get_user_by_email(email)
    if existing:
        return jsonify({"error": "User already exists"}), 400

    user_id = create_user(email, password)
    session["user_id"] = user_id

    log_event(user_id, "signup", {"email_domain": email.split("@")[-1] if "@" in email else None})

    return jsonify({"message": "Signup successful", "user_id": user_id})


@app.post("/api/login")
def api_login():
    data = request.get_json(force=True)
    email = data.get("email", "").strip()
    password = data.get("password", "")

    user = get_user_by_email(email)
    if not user or not verify_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user["id"]

    log_event(user["id"], "login")

    return jsonify({"message": "Login successful", "user_id": user["id"]})


@app.post("/api/logout")
def api_logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.get("/api/me")
def api_me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"user": None})

    personal = get_personal(user_id)
    return jsonify({
        "user": {
            "id": user_id,
            "first_name": personal["first_name"] if personal else None,
            "last_name": personal["last_name"] if personal else None,
            "country": personal["country"] if personal else None,
            "timezone": personal["timezone"] if personal else None,
        }
    })


@app.post("/api/personal")
def api_personal():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    country = (data.get("country") or "").strip() or None
    timezone = (data.get("timezone") or "").strip() or None

    upsert_personal(user_id, first_name, last_name, country, timezone)

    log_event(user_id, "personal_saved", {
        "has_first_name": bool(first_name),
        "has_last_name": bool(last_name),
        "has_country": bool(country),
        "has_timezone": bool(timezone)
    })

    return jsonify({"message": "Personal details saved"})

@app.get("/api/profile")
def api_get_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    prof = get_profile(user_id)
    return jsonify({"profile": dict(prof) if prof else None})


@app.post("/api/profile")
@login_required
def api_save_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    monthly = float(data.get("monthly_invest_amount", 0) or 0)
    risk = data.get("risk_appetite", "balanced")
    horizon = data.get("time_horizon", "long")
    markets = data.get("markets", "US stocks, ETFs")
    experience = data.get("experience_level", "beginner")

    if monthly <= 0:
        return jsonify({"error": "Monthly invest amount must be > 0"}), 400

    upsert_profile(user_id, monthly, risk, horizon, markets, experience)

    log_event(user_id, "profile_saved", {
        "risk_appetite": risk,
        "time_horizon": horizon,
        "experience_level": experience
    })

    return jsonify({"message": "Investment profile saved"})

@app.post("/api/plan/daily")
@login_required
def api_daily_plan():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    prof = get_profile(user_id)
    if not prof:
        return jsonify({"error": "Please set your investment profile first"}), 400

    data = request.get_json(force=True) if request.data else {}
    note = (data.get("note") or "").strip()

    # MVP: just return a disciplined routine plan
    investor_type = classify_investor(dict(prof))
    alloc = allocation(dict(prof))
    rules = principles(dict(prof))

    context_json = json.dumps({
        "investor_type": investor_type,
        "monthly_invest_amount": prof["monthly_invest_amount"],
        "risk_appetite": prof["risk_appetite"],
        "time_horizon": prof["time_horizon"],
        "allocation": alloc,
        "principles": rules,
        "user_note": note
    })


    prompt = f"""
    You are a disciplined investment advisor.

    Investor type: {investor_type}
    Monthly investment amount: {prof['monthly_invest_amount']}
    Time horizon: {prof['time_horizon']}
    Risk appetite: {prof['risk_appetite']}

    Recommended allocation: {alloc}
    Core principles: {rules}

    User note (optional): {note}

    Generate a calm, reassuring daily investment guidance message.
    No stock picks. No predictions. No trading.
    """

    plan_text = call_llm("SYSTEM", prompt)


    # save_plan(user_id, "daily", note or "{}", plan_text)
    save_plan(user_id, "daily", context_json, plan_text, advisor_version="v1")

    log_event(user_id, "plan_daily_generated", {
        "note_length": len(note),
        "mvp_mode": True
    })

    return jsonify({"plan": plan_text})


@app.get("/api/plans")
def api_plans():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    rows = list_plans(user_id)
    return jsonify({"plans": [dict(r) for r in rows]})


@app.get("/api/plans/<int:plan_id>")
def api_plan_detail(plan_id: int):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    row = get_plan(user_id, plan_id)
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"plan": dict(row)})

if __name__ == "__main__":
    app.run(debug=True)
