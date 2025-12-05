#Цель работы

Создать простое клиент-серверное приложение на Python без серверных фреймворков.

Освоить работу с HTTPServer и маршрутизацию запросов.

Применять шаблонизатор Jinja2 для отображения данных.

Реализовать модели предметной области (User, Currency, UserCurrency, App, Author) с геттерами и сеттерами.

Структурировать код в соответствии с архитектурой MVC.

Получать данные о курсах валют через функцию get_currencies и отображать их пользователям.

Реализовать функциональность подписки пользователей на валюты и отображение динамики их изменения.

Научиться создавать тесты для моделей и серверной логики

##Описание предметной области

##Модели

###1. Author

name — имя автора

group — учебная группа

###2. App

name — название приложения

version — версия приложения

author — объект Author

###3. User

id — уникальный идентификатор

name — имя пользователя

###4. Currency

id — уникальный идентификатор

num_code — цифровой код

char_code — символьный код

name — название валюты

value — курс

nominal — номинал (за сколько единиц валюты указан курс)

###5. UserCurrency

id — уникальный идентификатор

user_id — внешний ключ к User

currency_id — внешний ключ к Currency

Реализует связь «много ко многим» между пользователями и валютами.

##Архитектура проекта (MVC)

```python
myapp/
├── models/
│ ├── __init__.py
│ ├── author.py
│ ├── app.py
│ ├── user.py
│ ├── currency.py
│ └── user_currency.py
├── templates/
│ ├── index.html
│ ├── users.html
│ └── currencies.html
├── static/
│ └── css, js, изображения
├── myapp.py
└── utils/
 ├── currencies_api.py # функция get_currencies
 └── char_codes.py # функция для получения кодов валют
```
 
##Описание реализации

###Как реализованы модели и их свойства (геттеры/сеттеры)

#Все модели реализованы с использованием геттеров и сеттеров через @property
```python
@property
def name(self):
    """Геттер для имени автора"""
    return self.__name

@name.setter
def name(self, name: str):
    """Сеттер для имени автора с валидацией"""
    name = name.strip()
    if type(name) is str and len(name) >= 2:
        self.__name = name
    else:
        raise ValueError('Ошибка при задании имени автора')
```
Реализация маршрутов и обработка запросов
```python
#Использование urlparse и parse_qs
parsed_url = urlparse(self.path)
path = parsed_url.path
params = parse_qs(parsed_url.query)

#Маршрутизация
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
```

##Шаблонизатор Jinja2

```python
# Создание Jinja2 окружения
env = Environment(
    loader=PackageLoader("myapp"),          # Загрузчик из пакета
    autoescape=select_autoescape()          # Автоматическое экранирование
)

# Загрузка шаблонов при запуске
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")
Интеграция get_currencies
```
