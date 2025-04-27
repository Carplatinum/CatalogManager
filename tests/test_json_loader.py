import json
from typing import List


class Product:
    """
    Класс для описания товара с атрибутами и проверкой цены.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация товара.

        Args:
            name (str): Название товара.
            description (str): Описание товара.
            price (float): Цена товара (должна быть > 0).
            quantity (int): Количество товара на складе.
        """
        self.name = name
        self.description = description
        self.__price = None  # приватный атрибут цены
        self.price = price  # установка через сеттер с проверкой
        self.quantity = quantity

    @property
    def price(self):
        """Получить цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Установить цену товара с проверкой на положительное значение."""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, product_dict):
        """
        Создать объект Product из словаря.

        Args:
            product_dict (dict): Словарь с ключами name, description, price, quantity.

        Returns:
            Product: Новый объект товара.
        """
        return cls(
            name=product_dict.get("name"),
            description=product_dict.get("description"),
            price=product_dict.get("price"),
            quantity=product_dict.get("quantity")
        )

    def __str__(self):
        """Строковое представление товара."""
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Сложение двух товаров по общей стоимости (цена * количество).

        Args:
            other (Product): Другой товар.

        Returns:
            float: Суммарная стоимость.
        """
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity


class Category:
    """
    Класс для описания категории товаров.
    Подсчитывает общее количество категорий и продуктов.
    """

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products=None):
        """
        Инициализация категории.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (list[Product], optional): Список продуктов.
        """
        self.name = name
        self.description = description
        self.__products: List[Product] = []  # приватный список продуктов
        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product):
        """Добавить продукт в категорию и увеличить счётчик."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Получить строку со списком всех продуктов категории."""
        return "".join(str(p) + "\n" for p in self.__products)

    @property
    def product_list(self) -> List[Product]:
        """Получить копию списка продуктов категории."""
        return self.__products.copy()

    def __str__(self):
        """Строковое представление категории с общим количеством продуктов."""
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загрузить категории и продукты из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        list[Category]: Список объектов категорий с продуктами.
    """
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
