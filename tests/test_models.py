import pytest

from src.models import Category, Product


@pytest.fixture
def new_telephon():
    return Product("Телефон", "Описание телефона", 100.0, 4)


def test_product_init(new_telephon):
    assert new_telephon.name == "Телефон"
    assert new_telephon.description == "Описание телефона"
    assert new_telephon.price == 100.0
    assert new_telephon.quantity == 4


@pytest.fixture
def new_category(new_telephon):
    Category.product_count = 0
    Category.category_count = 0
    return Category("Телефоны", "Описание категории", [new_telephon, new_telephon])


def test_category_init(new_category, new_telephon):
    assert new_category.name == "Телефоны"
    assert new_category.description == "Описание категории"
    assert new_category.products[0] == new_telephon
    assert new_category.products[1] == new_telephon
    assert new_category.product_count == 2
    assert new_category.category_count == 1
