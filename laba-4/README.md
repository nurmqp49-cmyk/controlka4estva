# TicketBook — учебная система бронирования билетов

Учебный Flask-проект для практической работы по тестированию ПО.

## Быстрый старт

```bash
pip install -r requirements.txt
python app.py
```

Откройте http://127.0.0.1:5000

## Тестовые аккаунты

| Роль | Email | Пароль |
|---|---|---|
| Пользователь | user@ticketbook.ru | user123 |
| Администратор | admin@ticketbook.ru | admin123 |

## Архитектура модулей

```
M1 Auth    → session_token ──┐
M2 Catalog → event_id   ─────┼──► M3 Booking → booking_id ──► M4 Payment
                              │                    ▲
                              └────────────────────┘
```

## Структура

```
ticketbook/
├── app.py                  # Flask приложение, регистрация blueprints
├── requirements.txt
├── modules/
│   ├── store.py            # Общее хранилище данных (in-memory)
│   ├── auth.py             # M1: регистрация / вход / выход
│   ├── catalog.py          # M2: афиша, фильтры, CRUD
│   ├── booking.py          # M3: создание и отмена броней
│   └── payment.py          # M4: оплата, подтверждение
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── auth/               login.html, register.html
│   ├── catalog/            list.html, detail.html, form.html
│   ├── booking/            create.html, my.html, admin_all.html
│   └── payment/            pay.html, confirmation.html
└── static/
    ├── css/main.css
    └── js/main.js
```
