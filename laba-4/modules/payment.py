"""M4 — Payment: оплата по booking_id, обновление статуса брони."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from modules.store import bookings, sessions, now_str

payment_bp = Blueprint("payment", __name__)


def _get_email():
    token = session.get("session_token")
    return sessions.get(token) if token else None


@payment_bp.route("/pay/<booking_id>", methods=["GET", "POST"])
def pay(booking_id):
    email = _get_email()
    if not email:
        flash("Войдите в систему.", "warning")
        return redirect(url_for("auth.login"))
    bk = bookings.get(booking_id)
    if not bk or bk["user_email"] != email:
        flash("Бронирование не найдено.", "danger")
        return redirect(url_for("booking.my_bookings"))
    if bk["status"] != "pending":
        flash("Это бронирование уже обработано.", "info")
        return redirect(url_for("booking.my_bookings"))

    if request.method == "POST":
        card = request.form.get("card_number", "").replace(" ", "")
        # simple mock validation
        if len(card) != 16 or not card.isdigit():
            flash("Неверный номер карты.", "danger")
            return render_template("payment/pay.html", booking=bk)
        # simulate payment success (in real life — call payment gateway)
        bk["status"]   = "paid"
        bk["paid_at"]  = now_str()
        flash("Оплата прошла успешно! Билеты отправлены на email.", "success")
        return redirect(url_for("payment.confirmation", booking_id=booking_id))

    return render_template("payment/pay.html", booking=bk)


@payment_bp.route("/confirmation/<booking_id>")
def confirmation(booking_id):
    email = _get_email()
    if not email:
        flash("Войдите в систему.", "warning")
        return redirect(url_for("auth.login"))
    bk = bookings.get(booking_id)
    if not bk or bk["user_email"] != email:
        flash("Бронирование не найдено.", "danger")
        return redirect(url_for("booking.my_bookings"))
    return render_template("payment/confirmation.html", booking=bk)
