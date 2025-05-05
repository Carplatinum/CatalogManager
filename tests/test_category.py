import pytest
from src.models import Category, Product, Smartphone, LawnGrass


class TestCategoryAddProduct:
    def test_add_valid_product(self):
        cat = Category("Категория", "Описание")
        p = Product("Товар", "Описание", 100, 1)
        s = Smartphone("Модель", "Описание", 1000, 2, 90, "X", 128, "Черный")
        g = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")

        cat.add_product(p)
        cat.add_product(s)
        cat.add_product(g)

        assert len(cat.product_list) == 3

    def test_add_invalid_product_raises(self):
        cat = Category("Категория", "Описание")
        with pytest.raises(TypeError):
            cat.add_product("Не продукт")

        with pytest.raises(TypeError):
            cat.add_product(123)

        with pytest.raises(TypeError):
            cat.add_product(None)


class TestCategoryStr:
    def test_category_str_and_products(self):
        p1 = Product("Товар1", "Описание1", 50, 2)
        p2 = Product("Товар2", "Описание2", 150, 3)
        cat = Category("Категория", "Описание", [p1, p2])
        assert str(cat) == "Категория, количество продуктов: 5 шт."

        products_str = cat.products
        assert str(p1) in products_str
        assert str(p2) in products_str


class TestCategoryMiddlePrice:
    def test_middle_price_with_products(self):
        p1 = Product("Товар1", "Описание1", 100, 2)
        p2 = Product("Товар2", "Описание2", 200, 3)
        category = Category("Категория", "Описание", [p1, p2])

        expected_middle_price = (p1.price + p2.price) / 2
        assert category.middle_price() == expected_middle_price

    def test_middle_price_empty_category(self):
        category = Category("Пустая категория", "Описание", [])
        assert category.middle_price() == 0
