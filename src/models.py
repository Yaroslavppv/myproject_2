class Product:
    """
    Класс для продуктов
    """
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, descriptions: str, price: float, quantity: int):
        """
        Инициализация клосса
        :param name: Название продукта
        :param descriptions: Описание продукта
        :param price: Цена продукта
        :param quantity: Кол-во продукта
        """
        self.name = name
        self.description = descriptions
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс для категорий продуктов
    """
    name: str
    description: str
    products: list
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
        self.products = products
        Category.product_count += len(products)
        Category.category_count += 1
