from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseProduct(ABC):
    """
    Базовый абстрактный класс для продуктов
    """

    name: str
    description: str
    _price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация класса
        :param name: Имя
        :param description: Описание
        :param price:  Цена
        :param quantity: Кол-во
        """
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        super().__init__()

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Товар с нулевым или отрицательным количеством не может быть добавлен")
        self._quantity = value

    @abstractmethod
    def __str__(self) -> str:
        """
        Абстрактный метод для использования в наследуемых классах
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other: BaseProduct) -> float:
        """
        Абстрактный метод для использования в наследуемых классах
        :param other:
        :return:
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def price(self) -> float:
        """
        Абстрактный метод для использования в наследуемых классах
        :return:
        """
        raise NotImplementedError

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        """
        Абстрактный метод для использования в наследуемых классах
        :param new_price:
        :return:
        """
        raise NotImplementedError


class MixinProduct:
    """
    Миксин класс для отоброжения информации о продукте
    """

    def __init__(self, *args: Any) -> None:
        """
        Инициализация метода
        :param args:
        """
        print(repr(self))

    def __repr__(self) -> str:
        """
        Вывод информации о продукте
        :return: информации о продукте
        """
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(BaseProduct, MixinProduct):
    """
    Класс для продуктов
    """

    __instances: list[Product] = []

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация класса
        :param name: Название продукта
        :param descriptions: Описание продукта
        :param price: Цена продукта
        :param quantity: Кол-во продукта
        """
        super().__init__(name, description, price, quantity)
        self.__instances.append(self)

    def __str__(self) -> str:
        """
        Возвращает информацию о категории в строке
        :return: Строка в формате 'Название, количество продуктов: X шт.'
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity}"

    def __add__(self, other: Product) -> float:
        """
        Сложение двух продукторв
        :param other: Другой продукт
        :return: Суммарная стоимость 2-х продуктов
        """
        if type(self) is not type(other):
            raise TypeError
        else:
            sum_1 = self._price * self.quantity
            sum_2 = other._price * other.quantity
            return sum_1 + sum_2

    @classmethod
    def new_product(cls, product_dict: dict) -> Product:
        """
        Добавление(обновление) нового продукта из словаря
        :param product_dict: словарь
        :return: Новый продукт или обновление старого
        """
        for product in cls.__instances:
            if product.name == product_dict["name"]:
                product.quantity += product_dict["quantity"]
                product.price = max(product.price, product_dict["price"])
                return product
        return cls(product_dict["name"], product_dict["description"], product_dict["price"], product_dict["quantity"])

    @property
    def price(self) -> float:
        """
        Отображение цены товара
        :return: цена товара
        """
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Изменение цены товара
        :param new_price: новая цена
        :return:
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            if self._price > new_price:
                user_input = input("Введите подтверждение для снижения цены: Для подтверждения - Y\n")
                if user_input.lower() == "y":
                    self._price = new_price
            else:
                self._price = new_price


class Smartphone(Product):
    """
    Класс для смартфонов
    """

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self,
        name: str,
        descriptions: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        """
        Инициализация классса
        :param name: Название
        :param descriptions: Описание
        :param price: Цена
        :param quantity: Кол-во
        :param efficiency: Производительность
        :param model: Модель
        :param memory: Память
        :param color: Цвет
        """
        super().__init__(name, descriptions, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Класс для газонной травы
    """

    country: str
    germination_period: str
    color: str

    def __init__(
        self,
        name: str,
        descriptions: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        """
        Инициализация класса
        :param name: Название
        :param descriptions: Описание
        :param price: Цена
        :param quantity: Кол-во
        :param country: Страна
        :param germination_period: Срок проростания
        :param color: Цвет
        """
        super().__init__(name, descriptions, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class BaseCategory(ABC):
    """
    Базовый абстрактный класс для категорий
    """

    @abstractmethod
    def add_product(self, product: Product) -> None:
        """
        Абстрактный метод для использования в наследуемых классах
        :param product:
        :return:
        """
        raise NotImplementedError


class Category(BaseCategory):
    """
    Класс для категорий продуктов
    """

    name: str
    description: str
    __products: list
    product_count: int = 0
    category_count: int = 0

    def __init__(self, name: str, description: str, products: list):
        """
        Инициализация класса
        :param name: Название категории
        :param description: Описание категории
        :param products: Продукты в категории
        """
        self.name = name
        self.description = description
        self.__products = products
        Category.product_count += len(products)
        Category.category_count += 1

    def __str__(self) -> str:
        """
        Возвращает информацию о категории в строке
        :return: Строка формата 'Название категории, количество продукторв: X шт.'
        """
        product_quantity = 0
        for product in self.__products:
            product_quantity += product.quantity
        return f"{self.name}, количество продуктов: {product_quantity} шт."

    @property
    def products(self) -> list:
        """
        Отображение списка товаров в категории
        :return: Товары в категории
        """
        list_products = []
        for product in self.__products:
            list_products.append(f"{str(product)}")
        return list_products

    def add_product(self, product: Product) -> None:
        """
        Добавление нового продукта в категорию
        :param product: Продукт для добавления
        :return:
        """
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError

    def middle_price(self) -> float:
        """
        Высчитываение среднего ценника по категории
        :return: средняя цена по категории
        """
        try:
            products_sum = sum(product.price for product in self.__products)
            return products_sum / len(self.__products)
        except ZeroDivisionError:
            return 0.0


class Order(BaseCategory):
    """
    Класс заказов
    """

    product: Product | None
    quantity: int
    price: float
    total_price: float

    def __init__(self):
        """
        Инициализация класса
        """
        self.product = None
        self.total_price = 0
        self.price = 0
        self.quantity = 0

    def add_product(self, product: Product) -> None:
        """
        Добавление продукта в заказ
        :param product: Продукт
        :return:
        """
        if isinstance(product, Product):
            self.product = product
            self.price = product.price
        else:
            raise TypeError

    def add_quantity(self, quantity: int):
        """
        Добавление кол-ва продуктов в заказ
        :param quantity: Кол-во
        :return:
        """
        if quantity > 0:
            if quantity > self.product.quantity:
                raise ValueError("На складе недостаточно товара")
            else:
                self.quantity = quantity
                self.total_price = self.quantity * self.price
        else:
            raise ValueError("Значение не может быть меньше или равно 0")


class RangeCategory:
    """
    Итератор, возвращающий поочередно продукты из категории
    """

    category: Category
    stop: int

    def __init__(self, category: Category):
        """
        Инициализация класса
        :param category: Категория для перебора
        """
        self.category = category
        self.stop = len(category.products)

    def __iter__(self) -> "RangeCategory":
        """
        Возвращение итератора
        :return:
        """
        self.current_value = 0
        return self

    def __next__(self) -> Any:
        """
        Возвращает следующий продукт в категории
        :return: следующий продукт
        """
        product_list = self.category.products
        if self.current_value < self.stop:
            product = product_list[self.current_value]
            self.current_value += 1
            return product
        else:
            raise StopIteration
