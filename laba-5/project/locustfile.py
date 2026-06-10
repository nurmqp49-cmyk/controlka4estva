from locust import HttpUser, task, between

class ShopUser(HttpUser):
    wait_time = between(1, 3) # Пауза между кликами пользователя (от 1 до 3 сек)
    host = 'https://www.demoblaze.com'

    @task(3) # Вес 3 — выполняется чаще всего
    def view_homepage(self):
        with self.client.get('/', catch_response=True) as r:
            if r.status_code != 200:
                r.failure(f'Главная: ожидался 200, получен {r.status_code}')

    @task(2)
    def view_category(self):
        # Эмуляция отправки POST-запроса на бэкенд для фильтрации по категории
        self.client.post('/bycat', json={'cat': 'phone'})

    @task(1)
    def view_product(self):
        # Эмуляция просмотра карточки конкретного товара
        self.client.post('/view', json={'id': '1'})

    @task(1)
    def check_cart(self):
        # Эмуляция просмотра корзины покупок
        self.client.post('/viewcart', json={'cookie': 'guest', 'flag': True})