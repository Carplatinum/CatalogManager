import pytest

from src.models import Category, LawnGrass, Product, Smartphone


class TestProductPrice:
    def test_price_getter_and_setter_positive(self):
        p = Product("Телефон", "Смартфон", 10000, 5)
        assert p.price == 10000

        p.price = 15000
        assert p.price == 15000

    def test_price_setter_negative_or_zero(self, capsys):
        p = Product("Телефон", "Смартфон", 10000, 5)

        p.price = -500
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 10000  # Цена не изменилась

        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 10000  # Цена не изменилась

    def test_price_setter_positive_again(self):
        p = Product("Товар", "Описание", 100, 1)
        p.price = 200
        assert p.price == 200

    def test_price_setter_negative_or_zero_again(self, capsys):
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
    def test_new_product_creates_instance(self):
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
    def test_add_same_class_products(self):
        p1 = Product("Товар1", "Описание1", 100, 5)
        p2 = Product("Товар2", "Описание2", 200, 3)
        assert p1 + p2 == 100 * 5 + 200 * 3

    def test_add_different_class_products_raises(self):
        s = Smartphone("Модель", "Описание", 1000, 2, 90, "X", 128, "Черный")
        g = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")
        with pytest.raises(TypeError):
            _ = s + g


class TestCategoryAddProduct:
    def test_add_valid_product(self):
        cat = Category("Категория", "Описание")
        p = Product("Товар", "Описание", 100, 1)
        s = Smartphone("Модель", "Описание", 1000, 2, 90, "X", 128, "Черный")
        g = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")

        # Добавляем разные объекты-наследники Product без ошибок
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


class TestProductStrAndAdd:
    def test_str_representation(self):
        p = Product("Товар", "Описание", 100, 5)
        assert str(p) == "Товар, 100 руб. Остаток: 5 шт."

    def test_addition_with_non_product_raises(self):
        p = Product("Товар", "Описание", 100, 5)
        with pytest.raises(TypeError):
            _ = p + 10


class TestCategoryStr:
    def test_category_str_and_products(self):
        p1 = Product("Товар1", "Описание1", 50, 2)
        p2 = Product("Товар2", "Описание2", 150, 3)
        cat = Category("Категория", "Описание", [p1, p2])
        assert str(cat) == "Категория, количество продуктов: 5 шт."

        products_str = cat.products
        assert str(p1) in products_str
        assert str(p2) in products_str
