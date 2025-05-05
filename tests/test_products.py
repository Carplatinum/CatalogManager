import pytest
import json
from src.models import Product, Smartphone, LawnGrass, load_categories_from_json


class TestProductQuantityValidation:
    """Тесты валидации количества товара при инициализации."""

    def test_product_with_zero_quantity_raises_value_error(self):
        """Проверка, что при quantity=0 выбрасывается ValueError с нужным сообщением."""
        with pytest.raises(ValueError) as exc_info:
            Product("Бракованный товар", "Неверное количество", 1000.0, 0)
        assert str(exc_info.value) == ("Товар"
                                       " с нулевым количеством не может быть добавлен")


class TestProductPrice:
    """Тесты геттера и сеттера свойства price."""

    def test_price_getter_and_setter_positive(self):
        """Проверка корректной установки и получения положительной цены."""
        p = Product("Телефон", "Смартфон", 10000, 5)
        assert p.price == 10000

        p.price = 15000
        assert p.price == 15000

    def test_price_setter_negative_or_zero(self, capsys):
        """Проверка, что при установке отрицательной или нулевой цены
        выводится предупреждение и цена не меняется."""
        p = Product("Телефон", "Смартфон", 10000, 5)

        p.price = -500
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 10000

        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 10000

    def test_price_setter_positive_again(self):
        """Проверка повторной установки положительной цены."""
        p = Product("Товар", "Описание", 100, 1)
        p.price = 200
        assert p.price == 200

    def test_price_setter_negative_or_zero_again(self, capsys):
        """Повторная проверка установки отрицательной и нулевой цены."""
        p = Product("Товар", "Описание", 100, 1)
        p.price = -10
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100

        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 100


class TestProductNewProductMethod:
    """Тесты метода класса new_product."""

    def test_new_product_creates_instance(self):
        """Проверка создания экземпляра Product из словаря."""
        data = {
            "name": "Ноутбук",
            "description": "Игровой ноутбук",
            "price": 50000,
            "quantity": 3
        }
        p = Product.new_product(data)
        assert isinstance(p, Product)
        assert p.name == "Ноутбук"
        assert p.description == "Игровой ноутбук"
        assert p.price == 50000
        assert p.quantity == 3


class TestProductAddition:
    """Тесты сложения товаров."""

    def test_add_same_class_products(self):
        """Проверка сложения товаров одного класса."""
        p1 = Product("Товар1", "Описание1", 100, 5)
        p2 = Product("Товар2", "Описание2", 200, 3)
        assert p1 + p2 == 100 * 5 + 200 * 3

    def test_add_different_class_products_raises(self):
        """Проверка, что сложение товаров разных классов вызывает TypeError."""
        s = Smartphone("Модель", "Описание", 1000, 2, 90, "X", 128, "Черный")
        g = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")
        with pytest.raises(TypeError):
            _ = s + g

    def test_addition_with_non_product_raises(self):
        """Проверка, что сложение с не-Product вызывает TypeError."""
        p = Product("Товар", "Описание", 100, 5)
        with pytest.raises(TypeError):
            _ = p + 10


class TestProductStr:
    """Тесты строкового представления товара."""

    def test_str_representation(self):
        """Проверка корректного строкового представления товара."""
        p = Product("Товар", "Описание", 100, 5)
        assert str(p) == "Товар, 100 руб. Остаток: 5 шт."


class TestSmartphoneAndLawnGrass:
    """Тесты наследников Product: Smartphone и LawnGrass."""

    def test_smartphone_creation_and_repr(self):
        """Проверка создания и repr смартфона."""
        s = Smartphone("Galaxy", "Флагман", 70000, 3, 95, "S23", 256, "Черный")
        assert s.name == "Galaxy"
        assert s.efficiency == 95
        assert "efficiency=95" in repr(s)
        assert "model='S23'" in repr(s)

    def test_lawngrass_creation_and_repr(self):
        """Проверка создания и repr газонной травы."""
        g = LawnGrass("Трава", "Газонная", 500, 10, "Россия", "7 дней", "Зеленый")
        assert g.country == "Россия"
        assert "country='Россия'" in repr(g)
        assert "germination_period='7 дней'" in repr(g)


class TestLoadCategoriesFromJson:
    """Тесты функции загрузки категорий из JSON."""

    def test_load_categories_from_json(self, tmp_path):
        """Проверка корректной загрузки категорий и продуктов из JSON-файла."""
        data = [
            {
                "name": "Категория1",
                "description": "Описание1",
                "products": [
                    {"name": "Товар1", "description": "Описание",
                     "price": 100, "quantity": 5},
                    {"name": "Товар2", "description": "Описание",
                     "price": 200, "quantity": 3}
                ]
            },
            {
                "name": "Категория2",
                "description": "Описание2",
                "products": []
            }
        ]
        file = tmp_path / "categories.json"
        file.write_text(json.dumps(data), encoding="utf-8")

        categories = load_categories_from_json(str(file))
        assert len(categories) == 2
        assert categories[0].name == "Категория1"
        assert len(categories[0].product_list) == 2
        assert categories[1].name == "Категория2"
        assert categories[1].product_list == []
