import pytest
from src.models import Product, Category


@pytest.fixture(autouse=True)
def reset_class_counters():
    # Сбрасываем счетчики перед каждым тестом, чтобы тесты были независимы
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Test Product", "Test Description", 999.99, 10)
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 999.99
    assert product.quantity == 10


def test_category_initialization():
    product1 = Product("Prod1", "Desc1", 100.0, 5)
    product2 = Product("Prod2", "Desc2", 200.0, 3)
    category = Category("Category1", "Description1", [product1, product2])

    assert category.name == "Category1"
    assert category.description == "Description1"
    assert isinstance(category.products, list)
    assert len(category.products) == 2
    assert all(isinstance(p, Product) for p in category.products)


def test_category_count_increments():
    assert Category.category_count == 0
    Category("Cat1", "Desc", [])
    assert Category.category_count == 1
    Category("Cat2", "Desc", [])
    assert Category.category_count == 2


def test_product_count_accumulates():
    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    p3 = Product("P3", "D3", 30.0, 3)

    assert Category.product_count == 0
    Category("Cat1", "Desc", [p1, p2])
    assert Category.product_count == 2
    Category("Cat2", "Desc", [p3])
    assert Category.product_count == 3


def test_product_and_category_counts_together():
    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)

    assert Category.category_count == 0
    assert Category.product_count == 0

    Category("Cat1", "Desc", [p1])
    assert Category.category_count == 1
    assert Category.product_count == 1

    Category("Cat2", "Desc", [p2])
    assert Category.category_count == 2
    assert Category.product_count == 2
