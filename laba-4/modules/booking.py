"""M3 — Booking: создание и отмена бронирований."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from modules.store import events, bookings, sessions, new_id, now_str

booking_bp = Blueprint("booking", __name__)


def _get_user():
    token = session.get("session_token")
    if not token or token not in sessions:
        return None, None
    email = sessions[token]
    return token, email


@booking_bp.route("/create/<event_id>", methods=["GET", "POST"])
def create_booking(event_id):
    token, email = _get_user()
    if not email:
        flash("Войдите в систему, чтобы забронировать билет.", "warning")
        return redirect(url_for("auth.login"))
    ev = events.get(event_id)
    if not ev:
        flash("Мероприятие не найдено.", "danger")
        return redirect(url_for("catalog.list_events"))
    if ev["seats_left"] <= 0:
        flash("Свободных мест нет.", "danger")
        return redirect(url_for("catalog.event_detail", event_id=event_id))

    if request.method == "POST":
        qty = int(request.form.get("quantity", 1))
        if qty < 1 or qty > ev["seats_left"]:
            flash("Некорректное количество билетов.", "danger")
            return redirect(url_for("booking.create_booking", event_id=event_id))
        bid = new_id("bk")
        bookings[bid] = {
            "id":            bid,
            "event_id":      event_id,
            "event_title":   ev["title"],
            "event_date":    ev["date"],
            "event_time":    ev["time"],
            "venue":         ev["venue"],
            "user_email":    email,
            "session_token": token,
            "quantity":      qty,
            "total_price":   ev["price"] * qty,
            "status":        "pending",
            "created_at":    now_str(),
        }
        ev["seats_left"] -= qty
        flash("Бронирование создано! Перейдите к оплате.", "success")
        return redirect(url_for("payment.pay", booking_id=bid))

    return render_template("booking/create.html", event=ev)


@booking_bp.route("/cancel/<booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    _, email = _get_user()
    if not email:
        flash("Войдите в систему.", "warning")
        return redirect(url_for("auth.login"))
    bk = bookings.get(booking_id)
    if not bk or bk["user_email"] != email:
        flash("Бронирование не найдено.", "danger")
        return redirect(url_for("booking.my_bookings"))
    if bk["status"] == "paid":
        flash("Оплаченное бронирование нельзя отменить.", "danger")
        return redirect(url_for("booking.my_bookings"))
    # restore seats
    ev = events.get(bk["event_id"])
    if ev:
        ev["seats_left"] += bk["quantity"]
    bk["status"] = "cancelled"
    flash("Бронирование отменено.", "info")
    return redirect(url_for("booking.my_bookings"))


@booking_bp.route("/my")
def my_bookings():
    _, email = _get_user()
    if not email:
        flash("Войдите в систему.", "warning")
        return redirect(url_for("auth.login"))
    user_bks = [b for b in bookings.values() if b["user_email"] == email]
    user_bks.sort(key=lambda b: b["created_at"], reverse=True)
    return render_template("booking/my.html", bookings=user_bks)


@booking_bp.route("/admin/all")
def admin_all():
    if session.get("user_role") != "admin":
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("index"))
    all_bks = sorted(bookings.values(), key=lambda b: b["created_at"], reverse=True)
    return render_template("booking/admin_all.html", bookings=all_bks)
