import unittest
from app import app
from modules import store

class TicketBookIntegrationTests(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового окружения перед каждым тест-кейсом."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        # Очищаем временную базу данных броней перед тестом
        store.bookings.clear()

    def test_tc_int_01_and_04_success_booking_to_payment_flow(self):
        """Интеграционный тест цепочки M1 -> M3 -> M4 (Успешный сценарий)."""
        # Шаг 1: Авторизация (M1 Auth)
        login_response = self.client.post('/auth/login', data={
            'email': 'user@ticketbook.kz',
            'password': 'user123'
        }, follow_redirects=True)
        self.assertEqual(login_response.status_code, 200)
        
        # Шаг 2: Создание бронирования (M3 Booking)
        booking_form_response = self.client.post('/booking/create/evt-001', data={
            'quantity': 2
        }, follow_redirects=True)
        self.assertEqual(booking_form_response.status_code, 200)
        
        # Проверяем, что бронь физически создалась в хранилище данных store
        self.assertEqual(len(store.bookings), 1)
        booking_id = list(store.bookings.keys())[0]
        created_booking = store.bookings[booking_id]
        
        self.assertEqual(created_booking['status'], 'pending')
        self.assertEqual(created_booking['quantity'], 2)

        # Шаг 3: Проведение оплаты (M4 Payment)
        payment_response = self.client.post(f'/payment/pay/{booking_id}', data={
            'card_number': '1111222233334444'
        }, follow_redirects=True)
        self.assertEqual(payment_response.status_code, 200)
        
        # Проверяем интеграционное обновление статуса брони в модуле M3
        self.assertEqual(store.bookings[booking_id]['status'], 'paid')

    def test_tc_int_02_unauthorized_booking_rejection(self):
        """Проверка защиты модуля M3 от запросов неавторизованных пользователей."""
        response = self.client.post('/booking/create/evt-001', data={
            'quantity': 1
        }, follow_redirects=True)
        # Система должна перенаправить гостя на страницу аутентификации
        self.assertIn('Войти в систему', response.get_data(as_text=True))
        self.assertEqual(len(store.bookings), 0)

    def test_tc_int_03_non_existent_event_rejection(self):
        """Проверка поведения модуля M3 при получении невалидного event_id."""
        # Авторизуемся
        self.client.post('/auth/login', data={'email': 'user@ticketbook.kz', 'password': 'user123'})
        
        # Отправляем запрос на несуществующий ID мероприятия
        response = self.client.post('/booking/create/evt-99999', data={
            'quantity': 1
        }, follow_redirects=True)
        self.assertIn('Мероприятие не найдено.', response.get_data(as_text=True))
        self.assertEqual(len(store.bookings), 0)

    def test_tc_int_05_double_payment_protection(self):
        """Проверка блокировки повторной оплаты уже закрытого ордера."""
        # Авторизуемся и принудительно создаем оплаченную бронь в БД
        self.client.post('/auth/login', data={'email': 'user@ticketbook.kz', 'password': 'user123'})
        bid = "bk-test-double"
        store.bookings[bid] = {
            "id": bid, "event_id": "evt-001", "user_email": "user@ticketbook.kz",
            "quantity": 1, "total_price": 15000, "status": "paid"
        }
        
        # Пытаемся повторно отправить POST запрос на оплату этой брони
        response = self.client.post(f'/payment/pay/{bid}', data={
            'card_number': '1111222233334444'
        }, follow_redirects=True)
        self.assertIn('Это бронирование уже обработано.', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()