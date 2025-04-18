import json
import pytest
from src.data_loader import load_categories_from_json
from src.models import Category, Product


@pytest.fixture
def sample_json(tmp_path):
    # Создаем временный JSON файл с тестовыми данными
    data = [
        {
            "name": "Test Category",
            "description": "Test description",
            "products": [
                {
                    "name": "Test Product 1",
                    "description": "Desc 1",
                    "price": 100.0,
                    "quantity": 10
                },
                {
                    "name": "Test Product 2",
                    "description": "Desc 2",
                    "price": 200.0,
                    "quantity": 20
                }
            ]
        }
    ]
    file_path = tmp_path / "test_products.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False))
    return str(file_path)


def test_load_categories_from_json(sample_json):
    categories = load_categories_from_json(sample_json)

    assert isinstance(categories, list)
    assert len(categories) == 1

    category = categories[0]
    assert isinstance(category, Category)
    assert category.name == "Test Category"
    assert category.description == "Test description"
    assert isinstance(category.products, list)
    assert len(category.products) == 2

    product1 = category.products[0]
    product2 = category.products[1]

    assert isinstance(product1, Product)
    assert product1.name == "Test Product 1"
    assert product1.description == "Desc 1"
    assert product1.price == 100.0
    assert product1.quantity == 10

    assert isinstance(product2, Product)
    assert product2.name == "Test Product 2"
    assert product2.description == "Desc 2"
    assert product2.price == 200.0
    assert product2.quantity == 20
