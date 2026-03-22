from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import hashlib
from datetime import datetime
import requests as http_requests

app = Flask(__name__)
app.secret_key = "serl-demo-secret-key-change-in-production"

# ── Simple user store (file-based, no DB needed for demo) ──────────────
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── Rate limiter integration ───────────────────────────────────────────
RATE_LIMITER_URL = "http://localhost:8000/api/request"

def check_rate_limit(client_id: str) -> tuple[bool, dict]:
    """
    Calls your local SERL rate limiter before processing login/signup.
    If the rate limiter is offline, we ALLOW by default (fail open).
    """
    try:
        resp = http_requests.post(
            RATE_LIMITER_URL,
            json={"client_id": client_id},
            timeout=2
        )
        data = resp.json()
        allowed = resp.status_code == 200
        return allowed, data
    except Exception:
        # Rate limiter offline — fail open (allow request)
        return True, {"status": "limiter_offline"}

def get_client_id(req) -> str:
    """Uses IP + User-Agent as the client fingerprint."""
    ip = req.headers.get("X-Forwarded-For", req.remote_addr)
    return ip.split(",")[0].strip()

# ── Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        client_id = get_client_id(request)
        allowed, rl_info = check_rate_limit(client_id)

        if not allowed:
            flash("too_many", "error")
            return render_template("login.html", blocked=True, rl_info=rl_info), 429

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()

        if username in users and users[username]["password"] == hash_password(password):
            session["username"] = username
            session["login_time"] = datetime.utcnow().isoformat()
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")
            return render_template("login.html", blocked=False, error=True)

    return render_template("login.html", blocked=False)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        client_id = get_client_id(request)
        allowed, rl_info = check_rate_limit(client_id)

        if not allowed:
            flash("too_many", "error")
            return render_template("signup.html", blocked=True, rl_info=rl_info), 429

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")
        users = load_users()

        if not username or len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return render_template("signup.html", error="Username too short.")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("signup.html", error="Password too short.")
        if password != confirm:
            return render_template("signup.html", error="Passwords do not match.")
        if username in users:
            return render_template("signup.html", error="Username already taken.")

        users[username] = {
            "password": hash_password(password),
            "created": datetime.utcnow().isoformat()
        }
        save_users(users)
        session["username"] = username
        session["login_time"] = datetime.utcnow().isoformat()
        return redirect(url_for("dashboard"))

    return render_template("signup.html", blocked=False)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html",
        username=session["username"],
        login_time=session.get("login_time", "")
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)