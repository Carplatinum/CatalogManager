import pytest

from src.models import Category, Product


class TestProductStrAndAdd:
    @pytest.fixture
    def product_a(self):
        return Product("Товар A", "Описание A", 100, 10)

    @pytest.fixture
    def product_b(self):
        return Product("Товар B", "Описание B", 200, 2)

    def test_str_representation(self, product_a):
        expected_str = "Товар A, 100 руб. Остаток: 10 шт."
        assert str(product_a) == expected_str

    def test_addition_of_two_products(self, product_a, product_b):
        # 100*10 + 200*2 = 1000 + 400 = 1400
        assert product_a + product_b == 1400

    def test_addition_with_non_product(self, product_a):
        with pytest.raises(TypeError):
            _ = product_a + 5


class TestCategoryStr:
    @pytest.fixture
    def products(self):
        return [
            Product("Товар 1", "Описание 1", 50, 5),
            Product("Товар 2", "Описание 2", 150, 3),
            Product("Товар 3", "Описание 3", 200, 2),
        ]

    @pytest.fixture
    def category(self, products):
        return Category("Категория 1", "Описание категории", products)

    def test_str_representation(self, category):
        # Сумма количества: 5 + 3 + 2 = 10
        expected_str = "Категория 1, количество продуктов: 10 шт."
        assert str(category) == expected_str

    def test_products_property_returns_str_list(self, category, products):
        products_str = category.products
        for product in products:
            assert str(product) in products_str
