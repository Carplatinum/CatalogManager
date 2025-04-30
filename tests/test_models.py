import pytest

from src.models import Category, LawnGrass, Product, Smartphone


class TestCreationInfoMixin:
    def test_creation_prints_info(self, capsys):
        p = Product("Товар", "Описание", 100, 5)
        _ = repr(p)  # чтобы flake8 увидел использование переменной
        captured = capsys.readouterr()
        assert "Создан объект класса Product с параметрами" in captured.out

    def test_repr_product(self):
        p = Product("Товар", "Описание", 100, 5)
        expected_repr = ("Product(name='Товар', "
                         "description='Описание', price=100, quantity=5)")
        assert repr(p) == expected_repr

    def test_repr_smartphone(self):
        s = Smartphone("Телефон", "Смартфон", 1000, 2, 90, "X", 128, "Черный")
        expected_start = ("Smartphone(name='Телефон', "
                          "description='Смартфон', price=1000, quantity=2")
        expected_attrs = ["efficiency=90", "model='X'", "memory=128", "color='Черный'"]
        r = repr(s)
        assert r.startswith(expected_start)
        for attr in expected_attrs:
            assert attr in r

    def test_repr_lawngrass(self):
        g = LawnGrass("Трава", "Газон", 500, 10, "Россия", "7 дней", "Зеленый")
        expected_start = ("LawnGrass(name='Трава', "
                          "description='Газон', price=500, quantity=10")
        expected_attrs = ["country='Россия'",
                          "germination_period='7 дней'", "color='Зеленый'"]
        r = repr(g)
        assert r.startswith(expected_start)
        for attr in expected_attrs:
            assert attr in r


class TestProductFunctionality:
    def test_price_setter_positive(self):
        p = Product("Телефон", "Смартфон", 10000, 5)
        assert p.price == 10000
        p.price = 15000
        assert p.price == 15000

    def test_price_setter_negative(self, capsys):
        p = Product("Телефон", "Смартфон", 10000, 5)
        p.price = -500
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert p.price == 10000

    def test_addition_same_class(self):
        p1 = Product("Товар1", "Описание1", 100, 5)
        p2 = Product("Товар2", "Описание2", 200, 3)
        assert p1 + p2 == 100*5 + 200*3

    def test_addition_different_class_raises(self):
        s = Smartphone("Модель", "Описание", 1000, 2, 90, "X", 128, "Черный")
        g = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")
        with pytest.raises(TypeError):
            _ = s + g


class TestCategoryFunctionality:
    def test_add_product_and_counts(self):
        cat = Category("Категория", "Описание")
        p = Product("Товар", "Описание", 100, 1)
        s = Smartphone("Модель", "Описание", 1000, 2, 90, "X", 128, "Черный")
        g = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")

        cat.add_product(p)
        cat.add_product(s)
        cat.add_product(g)

        assert len(cat.product_list) == 3
        assert Category.product_count >= 3  # учитывая все тесты

    def test_add_invalid_product_raises(self):
        cat = Category("Категория", "Описание")
        with pytest.raises(TypeError):
            cat.add_product("Не продукт")
        with pytest.raises(TypeError):
            cat.add_product(123)
        with pytest.raises(TypeError):
            cat.add_product(None)
