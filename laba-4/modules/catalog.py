"""M2 — Catalog: список мероприятий, фильтрация, CRUD для админа."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from modules.store import events, new_id

catalog_bp = Blueprint("catalog", __name__)

CATEGORIES = {
    "concert": "Концерт",
    "theatre": "Театр",
    "cinema":  "Кино",
}


def _require_admin():
    return session.get("user_role") == "admin"


@catalog_bp.route("/")
def list_events():
    cat  = request.args.get("category", "")
    date = request.args.get("date", "")
    items = list(events.values())
    if cat:
        items = [e for e in items if e["category"] == cat]
    if date:
        items = [e for e in items if e["date"] == date]
    return render_template(
        "catalog/list.html",
        events=items,
        categories=CATEGORIES,
        selected_cat=cat,
        selected_date=date,
    )


@catalog_bp.route("/<event_id>")
def event_detail(event_id):
    ev = events.get(event_id)
    if not ev:
        flash("Мероприятие не найдено.", "danger")
        return redirect(url_for("catalog.list_events"))
    return render_template("catalog/detail.html", event=ev, categories=CATEGORIES)


# ── Admin CRUD ───────────────────────────────────────────────────────────────

@catalog_bp.route("/admin/create", methods=["GET", "POST"])
def create_event():
    if not _require_admin():
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("catalog.list_events"))
    if request.method == "POST":
        eid = new_id("evt")
        events[eid] = {
            "id":          eid,
            "title":       request.form["title"],
            "category":    request.form["category"],
            "date":        request.form["date"],
            "time":        request.form["time"],
            "venue":       request.form["venue"],
            "price":       int(request.form["price"]),
            "seats_total": int(request.form["seats_total"]),
            "seats_left":  int(request.form["seats_total"]),
            "image":       request.form.get("image", "concert.jpg"),
        }
        flash("Мероприятие создано.", "success")
        return redirect(url_for("catalog.list_events"))
    return render_template("catalog/form.html", event=None, categories=CATEGORIES, action="create")


@catalog_bp.route("/admin/edit/<event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if not _require_admin():
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("catalog.list_events"))
    ev = events.get(event_id)
    if not ev:
        flash("Мероприятие не найдено.", "danger")
        return redirect(url_for("catalog.list_events"))
    if request.method == "POST":
        ev.update({
            "title":    request.form["title"],
            "category": request.form["category"],
            "date":     request.form["date"],
            "time":     request.form["time"],
            "venue":    request.form["venue"],
            "price":    int(request.form["price"]),
        })
        flash("Мероприятие обновлено.", "success")
        return redirect(url_for("catalog.event_detail", event_id=event_id))
    return render_template("catalog/form.html", event=ev, categories=CATEGORIES, action="edit")


@catalog_bp.route("/admin/delete/<event_id>", methods=["POST"])
def delete_event(event_id):
    if not _require_admin():
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("catalog.list_events"))
    events.pop(event_id, None)
    flash("Мероприятие удалено.", "info")
    return redirect(url_for("catalog.list_events"))
