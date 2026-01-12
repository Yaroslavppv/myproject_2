from __future__ import annotations

from typing import Any


class Product:
    """
    Класс для продуктов
    """

    name: str
    description: str
    __price: float
    quantity: int
    __instances: list[Product] = []

    def __init__(self, name: str, descriptions: str, price: float, quantity: int):
        """
        Инициализация класса
        :param name: Название продукта
        :param descriptions: Описание продукта
        :param price: Цена продукта
        :param quantity: Кол-во продукта
        """
        self.name = name
        self.description = descriptions
        self.__price = price
        self.quantity = quantity
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
        sum_1 = self.__price * self.quantity
        sum_2 = other.__price * other.quantity
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
        return self.__price

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
            if self.__price > new_price:
                user_input = input("Введите подтверждение для снижения цены: Для подтверждения - Y\n")
                if user_input.lower() == "y":
                    self.__price = new_price
            else:
                self.__price = new_price


class Category:
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
        self.__products.append(product)
        self.product_count += 1


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
