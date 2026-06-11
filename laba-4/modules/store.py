import uuid, datetime

# ── Users ──────────────────────────────────────────────────────────────────
users = {
    "admin@ticketbook.kz": {
        "password": "admin123",
        "role": "admin",
        "name": "Администратор",
    },
    "user@ticketbook.kz": {
        "password": "user123",
        "role": "user",
        "name": "Пользователь",
    },
}

# active sessions:  session_token -> email
sessions: dict[str, str] = {}

# ── Events ─────────────────────────────────────────────────────────────────
events = {
    "evt-001": {
        "id": "evt-001",
        "title": "Концерт бтс",
        "category": "concert",
        "date": "2026-07-12",
        "time": "20:00",
        "venue": "Алматы Арена, Алматы",
        "price": 15000,
        "seats_total": 200,
        "seats_left": 143,
        "image": "concert.jpg",
    },
    "evt-002": {
        "id": "evt-002",
        "title": "Спектакль «хз»",
        "category": "theatre",
        "date": "2026-07-18",
        "time": "19:00",
        "venue": "ГАТОБ им. Абая, Алматы",
        "price": 8500,
        "seats_total": 150,
        "seats_left": 60,
        "image": "theatre.jpg",
    },
    "evt-003": {
        "id": "evt-003",
        "title": "Кино: «Backrooms»",
        "category": "cinema",
        "date": "2026-06-11",
        "time": "18:30",
        "venue": "Kinopark 11 IMAX, Астана",
        "price": 2500,
        "seats_total": 300,
        "seats_left": 210,
        "image": "cinema.jpg",
    },
    "evt-004": {
        "id": "evt-004",
        "title": "Фестиваль «Наурыз Думан»",
        "category": "concert",
        "date": "2026-08-02",
        "time": "14:00",
        "venue": "Парк Первого Президента, Астана",
        "price": 5000,
        "seats_total": 500,
        "seats_left": 380,
        "image": "concert.jpg",
    },
    "evt-005": {
        "id": "evt-005",
        "title": "Балет «какой-то»",
        "category": "theatre",
        "date": "2026-08-10",
        "time": "19:30",
        "venue": "Астана Опера, Астана",
        "price": 22000,
        "seats_total": 120,
        "seats_left": 22,
        "image": "theatre.jpg",
    },
    "evt-006": {
        "id": "evt-006",
        "title": "Stand-up: Нурлан Сабуров",
        "category": "comedy",
        "date": "2026-08-15",
        "time": "20:00",
        "venue": "Театр «Жас Сахна», Шымкент",
        "price": 9000,
        "seats_total": 250,
        "seats_left": 95,
        "image": "concert.jpg",
    },
}

# ── Bookings ────────────────────────────────────────────────────────────────
bookings: dict[str, dict] = {}

# ── Helpers ─────────────────────────────────────────────────────────────────
def new_id(prefix="id"):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"

def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")