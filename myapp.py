from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from models import Author, User, Currency, UserCurrency, App
from utils.currencies_api import get_currencies
from utils.char_codes import get_char_codes

# Jinja2 окружение
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

# Загрузка шаблонов
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")

main_author = Author("Яна Литвиновская", "Р3124")
app_instance = App("Вывод валют", "1.0", main_author)

# Получаем курсы валют (возвращает словарь {код: значение})
currency_codes = get_char_codes()
currency_values = get_currencies(currency_codes)

# Создаем объекты Currency из словаря
currencies = []
for code, data in currency_values.items():
    currency = Currency(
        id = data.get('id'),
        num_code = data.get('num_code'),
        char_code = code,
        name = data.get('name'),
        value = data.get('value'),
        nominal = data.get('nominal')
    )
    currencies.append(currency)

currency_by_code = {curr.char_code: curr for curr in currencies}

users = [
    User(1, "Никита Свин"),
    User(2, "Артем Рыба"),
    User(3, "Матвей Груб")
    ]

# Связи пользователей с валютами
user_currencies = []
popular_valute = ['USD', 'EUR']

cnt = 1
for us in users:
    for val_code in popular_valute:
        currency = currency_by_code[val_code]
        user_currencies.append(UserCurrency(
            id=cnt,
            user_id=us.id,
            currency_id=currency.id,
            user=us,
            currency=currency))
        cnt += 1

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Парсим URL с помощью urlparse
        parsed_url = urlparse(self.path)
        path = parsed_url.path  # Чистый путь без параметров
        params = parse_qs(parsed_url.query)  # Параметры запроса

        # Маршрутизация на основе распарсенного пути
        if path == '/' or path == '/index':
            self.show_index(params)
        elif path == '/users':
            self.show_users(params)
        elif path == '/user':
            self.show_user(params)
        elif path == '/currencies':
            self.show_currencies(params)
        else:
            self.send_error(404, "Страница не найдена")

    def show_index(self, params=None):
        """Главная страница"""

        result = template_index.render(
            myapp=app_instance.name,
            author_name=main_author.name,
            author_group=main_author.group,
            stats={
                'users_count': len(users),
                'currencies_count': len(currencies),
                'subscriptions_count': len(user_currencies)
            }
        )

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))

    def show_users(self, params=None):
        """Список пользователей"""
        user_id_str = params.get('user_id', [''])[0] if params else ''
        selected_user = None

        if user_id_str and user_id_str.isdigit():
            user_id = int(user_id_str)
            selected_user = next((u for u in users if u.id == user_id), None)

        # Подготавливаем список пользователей
        users_list = []
        for user in users:
            subs = [uc for uc in user_currencies if uc.user_id == user.id]
            users_list.append({
                'user': user,
                'subscriptions_count': len(subs),
                'currencies': [uc.currency.char_code for uc in subs if uc.currency]
            })

        #template = env.get_template("users.html")
        result = template_users.render(
            myapp=app_instance.name,
            users=users_list,
            selected_user=selected_user,
            user_subscriptions=[uc for uc in user_currencies if selected_user and uc.user_id == selected_user.id]
        )

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))

    def show_user(self, params=None):
        """Информация о пользователе (/user?id=...)"""
        user_id = params.get('id', [''])[0] if params else ''

        if user_id:
            # Перенаправляем на /users?user_id=...
            self.send_response(302)
            self.send_header('Location', f'/users?user_id={user_id}')
            self.end_headers()
        else:
            self.send_error(400, "Не указан ID пользователя")

    def show_currencies(self, params=None):
        """Список валют"""
        search = params.get('search', [''])[0] if params else ''

        # Фильтрация
        if search:
            filtered = []
            for currency in currencies:
                if (search.lower() in currency.name.lower() or
                        search.lower() in currency.char_code.lower()):
                    filtered.append(currency)
        else:
            filtered = currencies

        # Подготавливаем данные
        currencies_list = []
        for currency in filtered:
            users_count = len([uc for uc in user_currencies if uc.currency_id == currency.id])
            currencies_list.append({
                'currency': currency,
                'users_count': users_count
            })

        #template = env.get_template("currencies.html")
        result = template_currencies.render(
            myapp=app_instance.name,
            currencies=currencies_list,
            total=len(filtered),
            search_query=search
        )

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))

    def send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()

        error_text = f"Ошибка {code}: {message}\nПерейдите на /"
        self.wfile.write(error_text.encode("utf-8"))

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('=' * 50)
    print('Сервер запущен: http://localhost:8080')
    httpd.serve_forever()