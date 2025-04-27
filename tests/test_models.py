import pytest
from src.models import Category, Product


class TestProductStrAndAdd:
    """Тесты для строкового представления и сложения объектов Product."""

    @pytest.fixture
    def product_a(self):
        """Фикстура: продукт A с ценой 100 и количеством 10."""
        return Product("Товар A", "Описание A", 100, 10)

    @pytest.fixture
    def product_b(self):
        """Фикстура: продукт B с ценой 200 и количеством 2."""
        return Product("Товар B", "Описание B", 200, 2)

    def test_str_representation(self, product_a):
        """Проверка форматирования строки продукта (магазинное представление)."""
        expected_str = "Товар A, 100 руб. Остаток: 10 шт."
        assert str(product_a) == expected_str

    def test_addition_of_two_products(self, product_a, product_b):
        """Проверка сложения продуктов по формуле (price * quantity) для каждого."""
        assert product_a + product_b == 1400  # 100*10 + 200*2

    def test_addition_with_non_product(self, product_a):
        """Проверка выброса TypeError при попытке сложить Product с не-Product."""
        with pytest.raises(TypeError):
            _ = product_a + 5


class TestCategoryStr:
    """Тесты для строкового представления и свойств категорий."""

    @pytest.fixture
    def products(self):
        """Фикстура: список из трёх продуктов с разными характеристиками."""
        return [
            Product("Товар 1", "Описание 1", 50, 5),
            Product("Товар 2", "Описание 2", 150, 3),
            Product("Товар 3", "Описание 3", 200, 2),
        ]

    @pytest.fixture
    def category(self, products):
        """Фикстура: категория с тремя продуктами."""
        return Category("Категория 1", "Описание категории", products)

    def test_str_representation(self, category):
        """Проверка форматирования строки категории (общее количество продуктов)."""
        assert str(category) == "Категория 1, количество продуктов: 10 шт."

    def test_products_property_returns_str_list(self, category, products):
        """Проверка, что свойство products возвращает строковые представления продуктов."""
        products_str = category.products
        for product in products:
            assert str(product) in products_str
