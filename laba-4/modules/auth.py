"""M1 — Auth: регистрация, вход, выход, выдача session_token."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from modules.store import users, sessions, new_id, now_str

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        name  = request.form.get("name", "").strip()
        pwd   = request.form.get("password", "")
        if not email or not name or not pwd:
            flash("Заполните все поля.", "danger")
        elif email in users:
            flash("Пользователь с таким email уже существует.", "danger")
        else:
            users[email] = {"password": pwd, "role": "user", "name": name}
            flash("Регистрация успешна! Войдите в систему.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pwd   = request.form.get("password", "")
        user  = users.get(email)
        if user and user["password"] == pwd:
            token = new_id("tok")
            sessions[token] = email
            session["session_token"] = token
            session["user_email"]    = email
            session["user_name"]     = user["name"]
            session["user_role"]     = user["role"]
            flash(f"Добро пожаловать, {user['name']}!", "success")
            return redirect(url_for("index"))
        flash("Неверный email или пароль.", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    token = session.pop("session_token", None)
    if token:
        sessions.pop(token, None)
    session.clear()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("index"))
