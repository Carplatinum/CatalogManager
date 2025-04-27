import json
from typing import List


class Product:
    """
    Класс для описания товара.

    Атрибуты:
        name (str): Название товара.
        description (str): Описание товара.
        price (float): Цена товара (приватный атрибут с проверкой при установке).
        quantity (int): Количество товара на складе.

    Методы:
        __init__(name, description, price, quantity): Инициализирует объект Product с проверкой цены.
    """
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = None  # приватный атрибут цены
        self.price = price   # установка через сеттер с проверкой
        self.quantity = quantity


    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой"""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, product_dict):
        """Создаёт новый продукт из словаря"""
        return cls(
            name=product_dict.get("name"),
            description=product_dict.get("description"),
            price=product_dict.get("price"),
            quantity=product_dict.get("quantity")
        )

    def __str__(self):
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products=None):
        self.name = name
        self.description = description
        self.__products: List[Product] = []  # приватный атрибут списка продуктов
        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product):
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер, возвращающий строку со списком продуктов"""
        return "".join(str(p) + "\n" for p in self.__products)

    @property
    def product_list(self) -> List[Product]:
        """Геттер, возвращающий копию списка продуктов"""
        return self.__products.copy()

    def __str__(self):
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


def load_categories_from_json(file_path: str) -> List[Category]:
    """Загрузка данных из JSON-файла и создание объектов категорий"""
    categories = []

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for category_data in data:
            category = Category(
                name=category_data['name'],
                description=category_data['description']
            )

            for product_data in category_data.get('products', []):
                product = Product.new_product(product_data)
                category.add_product(product)

            categories.append(category)

    return categories
