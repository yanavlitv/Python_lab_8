class Currency:
    def __init__(self, id: str, num_code: int, char_code: str, name: str, value: float, nominal: int):
        self.__id: str = id
        self.__num_code: int = num_code
        self.__char_code: str = char_code
        self.__name: str = name
        self.__value: float = value
        self.__nominal: int = nominal

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        id = id.strip()
        if type(id) is str and len(id) > 0:
            self.__id = id.strip()
        else:
            raise ValueError('ID валюты должен быть строкой')

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: int):
        if type(num_code) is int and 1 <= num_code <= 999:
            self.__num_code = num_code
        else:
            raise ValueError('Цифровой код должен быть целым числом от 1 до 999')

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        char_code = char_code.strip()
        if type(char_code) is str and len(char_code) == 3 and char_code.isalpha():
            self.__char_code = char_code.upper()
        else:
            raise ValueError('Символьный код должен состоять из 3 букв')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        name = name.strip()
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Название валюты должно быть строкой длиной не менее 2 символов')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: float):
        if type(value) is float and value > 0:
            self.__value = float(value)
        else:
            raise ValueError('Курс валюты должен быть положительным числом')

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if type(nominal) is int and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError('Номинал должен быть положительным целым числом')

    def __str__(self):
        """Для пользователя - более читаемо"""
        return f"{self.__char_code} - {self.__name} ({self.__value} руб. за {self.__nominal} ед.)"

    def __repr__(self):
        """Для разработчика - полная информация"""
        return (f"Currency(id={self.__id!r}, num_code={self.__num_code}, "
            f"char_code={self.__char_code!r}, name={self.__name!r}, "
            f"value={self.__value}, nominal={self.__nominal})")