from typing import Any

import pytest

from src.models import Category, LawnGrass, Product, RangeCategory, Smartphone


@pytest.fixture
def new_telephon() -> Product:
    return Product("Телефон", "Описание телефона", 100.0, 4)


@pytest.fixture
def clean_instances() -> None:
    instances: list = getattr(Product, "_Product__instances")
    instances.clear()


def test_product_init(new_telephon: Product) -> None:
    assert new_telephon.name == "Телефон"
    assert new_telephon.description == "Описание телефона"
    assert new_telephon.price == 100.0
    assert new_telephon.quantity == 4


def test_product_str(new_telephon: Product) -> None:
    assert str(new_telephon) == "Телефон, 100.0 руб. Остаток: 4"


def test_product_add(new_telephon: Product, new_lawngrass: LawnGrass, new_smartphone: Smartphone) -> None:
    assert new_telephon + new_telephon == 800.0

    with pytest.raises(TypeError):
        new_lawngrass + new_smartphone


def test_new_product_create(clean_instances: Any) -> None:
    test_product = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
    new_product = Product.new_product(test_product)

    assert new_product.name == "Samsung Galaxy S23 Ultra"
    assert new_product.description == "256GB, Серый цвет, 200MP камера"
    assert new_product.quantity == 5
    instances: list = getattr(Product, "_Product__instances")
    assert len(instances) == 1


def test_new_product_update(clean_instances: Any, new_telephon: Product) -> None:
    test_product = {"name": "Телефон", "description": "Описание телефона", "price": 190000.0, "quantity": 5}

    update_product = Product.new_product(test_product)

    assert update_product.quantity == 9
    assert update_product.price == 190000.0
    instances: list = getattr(Product, "_Product__instances")
    assert len(instances) == 1


def test_new_product_update_lower_price(clean_instances: Any, new_telephon: Product) -> None:
    test_product = {"name": "Телефон", "description": "Описание телефона", "price": 5.0, "quantity": 5}

    update_product = Product.new_product(test_product)

    assert update_product.quantity == 9
    assert update_product.price == 100.0
    instances: list = getattr(Product, "_Product__instances")
    assert len(instances) == 1


@pytest.mark.parametrize(
    "test_price, test_message, expected",
    [(140.4, 140.4, None), (-10, "Цена не должна быть нулевая или отрицательная\n", True), (5.0, 5.0, "Patch")],
)
def test_new_product_setter(
    new_telephon: Product,
    capsys: Any,
    test_price: float,
    test_message: float | str,
    expected: None | str | bool,
    monkeypatch: Any,
) -> None:
    if expected is None:
        new_telephon.price = test_price
        assert new_telephon.price == test_message
    elif expected == "Patch":
        monkeypatch.setattr("builtins.input", lambda _: "Y")
        new_telephon.price = test_price
        assert new_telephon.price == test_message
    else:
        new_telephon.price = test_price
        captured = capsys.readouterr()
        assert captured.out == test_message


@pytest.fixture
def new_smartphone() -> Smartphone:
    return Smartphone("Телефон", "Описание", 100.0, 5, 95.5, "Модель", 256, "Цвет")


def test_smartphone_init(new_smartphone: Smartphone) -> None:
    assert new_smartphone.name == "Телефон"
    assert new_smartphone.description == "Описание"
    assert new_smartphone.price == 100.0
    assert new_smartphone.quantity == 5
    assert new_smartphone.efficiency == 95.5
    assert new_smartphone.model == "Модель"
    assert new_smartphone.memory == 256
    assert new_smartphone.color == "Цвет"


@pytest.fixture
def new_lawngrass() -> LawnGrass:
    return LawnGrass("Трава", "Описание", 500.0, 20, "Страна", "Срок проростания", "Цвет")


def test_lawngrass_init(new_lawngrass: LawnGrass) -> None:
    assert new_lawngrass.name == "Трава"
    assert new_lawngrass.description == "Описание"
    assert new_lawngrass.price == 500.0
    assert new_lawngrass.quantity == 20
    assert new_lawngrass.country == "Страна"
    assert new_lawngrass.germination_period == "Срок проростания"
    assert new_lawngrass.color == "Цвет"


@pytest.fixture
def new_category(new_telephon: Product) -> Category:
    Category.product_count = 0
    Category.category_count = 0
    return Category("Телефоны", "Описание категории", [new_telephon, new_telephon])


def test_category_init(new_category: Category, new_telephon: Product) -> None:
    assert new_category.name == "Телефоны"
    assert new_category.description == "Описание категории"
    assert new_category.products == ["Телефон, 100.0 руб. Остаток: 4", "Телефон, 100.0 руб. Остаток: 4"]
    assert new_category.product_count == 2
    assert new_category.category_count == 1


def test_add_product(new_category: Category, new_telephon: Product) -> None:
    new_category.add_product(new_telephon)
    assert new_category.products == [
        "Телефон, 100.0 руб. Остаток: 4",
        "Телефон, 100.0 руб. Остаток: 4",
        "Телефон, 100.0 руб. Остаток: 4",
    ]
    assert new_category.product_count == 3

    with pytest.raises(TypeError):
        new_category.add_product("Продукт") # type: ignore


def test_category_str(new_category: Category) -> None:
    assert str(new_category) == "Телефоны, количество продуктов: 8 шт."


@pytest.fixture
def new_rangecategory(new_category: Category) -> RangeCategory:
    return RangeCategory(new_category)


def test_rangecategory_init(new_rangecategory: RangeCategory, new_category: Category) -> None:
    assert new_rangecategory.category == new_category
    assert new_rangecategory.stop == len(new_category.products)


def test_rangecategory_iteration(new_rangecategory: RangeCategory) -> None:
    iterator = iter(new_rangecategory)

    first_item = next(iterator)
    assert first_item == "Телефон, 100.0 руб. Остаток: 4"

    second_item = next(iterator)
    assert second_item == "Телефон, 100.0 руб. Остаток: 4"

    with pytest.raises(StopIteration):
        next(iterator)
