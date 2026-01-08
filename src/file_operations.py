import json
from pathlib import Path

from src.models import Category, Product

file_operations = Path(__file__).parent.parent / "data" / "products.json"


def read_json(file: str):
    """
    Функция считывания из json файла
    :param file: путь к файлу
    :return: возвращает список категорий и продуктов
    """
    with open(file, "r", encoding="utf-8") as f:
        data_operations = json.load(f)
    product_list = []
    category_list = []
    last_index = 0
    for category in data_operations:
        for product in category["products"]:
            product_list.append(
                Product(
                    str(product["name"]),
                    str(product["description"]),
                    float(product["price"]),
                    int(product["quantity"]),
                )
            )
        category_list.append(Category(str(category["name"]), str(category["description"]), product_list[last_index:]))
        last_index = len(product_list)
    return product_list, category_list
