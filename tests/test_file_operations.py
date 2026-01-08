import json
from unittest.mock import mock_open, patch

import src.file_operations


def test_read_json() -> None:
    mock_data = [
        {
            "name": "Смартфоны",
            "description": "Смартфоны, как средство не только коммуникации, "
                           "но и получение дополнительных функций для удобства жизни",
            "products": [
                {
                    "name": "Samsung Galaxy C23 Ultra",
                    "description": "256GB, Серый цвет, 200MP камера",
                    "price": 180000.0,
                    "quantity": 5,
                },
                {"name": "Iphone 15", "description": "512GB, Gray space", "price": 210000.0, "quantity": 8},
                {"name": "Xiaomi Redmi Note 11", "description": "1024GB, Синий", "price": 31000.0, "quantity": 14},
            ],
        },
        {
            "name": "Телевизоры",
            "description": "Современный телевизор, который позволяет "
                           "наслаждаться просмотром, станет вашим другом и помощником",
            "products": [
                {"name": '55" QLED 4K', "description": "Фоновая подсветка", "price": 123000.0, "quantity": 7}
            ],
        },
    ]
    test_json = json.dumps(mock_data)
    with patch("src.file_operations.open", mock_open(read_data=test_json)):
        test_products, test_categories = src.file_operations.read_json("fake_path.json")

    assert len(test_products) == 4
    assert test_products[0].name == "Samsung Galaxy C23 Ultra"
    assert test_products[1].description == "512GB, Gray space"
    assert len(test_categories) == 2
    assert test_categories[1].category_count == 2
    assert test_categories[0].products[2].name == "Xiaomi Redmi Note 11"
