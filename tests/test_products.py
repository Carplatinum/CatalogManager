from src.models import Product


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
