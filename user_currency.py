from models.user import User
from models.currency import Currency


class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: str, user: User = None, currency: Currency = None):
        self.__id: int = id
        self.__user_id: int = user_id
        self.__currency_id: str = currency_id
        self.__user: User = user
        self.__currency: Currency = currency

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if type(id) is int and id > 0:
            self.__id = id
        else:
            raise ValueError('ID должен быть положительным целым числом')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if type(user_id) is int and user_id > 0:
            self.__user_id = user_id
        else:
            raise ValueError('user_id должен быть положительным целым числом')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: str):
        currency_id = currency_id.strip()
        if type(currency_id) is str and len(currency_id) > 0:
            self.__currency_id = currency_id.strip()
        else:
            raise ValueError('currency_id должен быть непустой строкой')

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: User):
        if user is None or type(user) is User:
            self.__user = user
        elif type(user) is User:
            self.__user = user
            self.__user_id = user.id
        else:
            raise ValueError('user должен быть объектом типа User или None')

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, currency: Currency):
        if currency is None or type(currency) is Currency:
            self.__currency = currency
            if currency is not None:
                self.__currency_id = currency.id
        else:
            raise ValueError('currency должен быть объектом типа Currency или None')

    def __str__(self):
        user_info = self.__user.name if self.__user else f"id={self.__user_id}"
        currency_info = self.__currency.char_code if self.__currency else f"id='{self.__currency_id}'"
        return f"UserCurrency(id={self.__id}, user={user_info}, currency={currency_info})"

    def __repr__(self):
        return self.__str__()