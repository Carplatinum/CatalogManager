import pytest
from src.models import Category, Product


class TestCategoryAddProduct:
    """Тесты добавления продуктов в категорию."""

    def test_add_valid_product(self):
        """Проверка успешного добавления валидного продукта."""
        cat = Category("Категория", "Описание")
        p = Product("Товар", "Описание", 100, 1)
        cat.add_product(p)
        assert len(cat.product_list) == 1

    def test_add_invalid_product_raises(self):
        """Проверка, что при добавлении невалидных объектов выбрасывается TypeError."""
        cat = Category("Категория", "Описание")
        with pytest.raises(TypeError):
            cat.add_product("Не продукт")
        with pytest.raises(TypeError):
            cat.add_product(123)
        with pytest.raises(TypeError):
            cat.add_product(None)
        with pytest.raises(TypeError):
            cat.add_product(3.14)
        with pytest.raises(TypeError):
            cat.add_product(object())


class TestCategoryStr:
    """Тесты строкового представления категории."""

    def test_category_str_and_products(self):
        """Проверка корректного строкового представления категории
        и списка продуктов."""
        p1 = Product("Товар1", "Описание1", 50, 2)
        p2 = Product("Товар2", "Описание2", 150, 3)
        cat = Category("Категория", "Описание", [p1, p2])
        assert str(cat) == "Категория, количество продуктов: 5 шт."
        products_str = cat.products
        assert str(p1) in products_str
        assert str(p2) in products_str


class TestCategoryMiddlePrice:
    """Тесты метода подсчёта средней цены товаров в категории."""

    def test_middle_price_with_products(self):
        """Проверка средней цены при наличии товаров."""
        p1 = Product("Товар1", "Описание1", 100, 2)
        p2 = Product("Товар2", "Описание2", 200, 3)
        category = Category("Категория", "Описание", [p1, p2])
        expected_middle_price = (p1.price + p2.price) / 2
        assert category.middle_price() == expected_middle_price

    def test_middle_price_empty_category(self):
        """Проверка, что для пустой категории возвращается 0."""
        category = Category("Пустая категория", "Описание", [])
        assert category.middle_price() == 0

    def test_middle_price_after_adding_products(self):
        """Проверка обновления средней цены после добавления товаров."""
        category = Category("Категория", "Описание")
        assert category.middle_price() == 0  # пустая категория
        p = Product("Товар", "Описание", 150, 1)
        category.add_product(p)
        assert category.middle_price() == 150

    def test_middle_price_with_one_product(self):
        """Проверка средней цены при одном товаре."""
        p = Product("Товар", "Описание", 123, 5)
        category = Category("Категория", "Описание", [p])
        assert category.middle_price() == 123
