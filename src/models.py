import json
from typing import List

class Product:
    """
    Базовый класс для описания товара.
    """
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = None
        self.price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(cls, product_dict):
        return cls(
            name=product_dict.get("name"),
            description=product_dict.get("description"),
            price=product_dict.get("price"),
            quantity=product_dict.get("quantity")
        )

    def __str__(self):
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного типа")
        return self.price * self.quantity + other.price * other.quantity

class Smartphone(Product):
    """
    Класс для описания смартфона.
    """
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

class LawnGrass(Product):
    """
    Класс для описания газонной травы.
    """
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products=None):
        self.name = name
        self.description = description
        self.__products: List[Product] = []
        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "".join(str(p) + "\n" for p in self.__products)

    @property
    def product_list(self) -> List[Product]:
        return self.__products.copy()

    def __str__(self):
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

def load_categories_from_json(file_path: str) -> List[Category]:
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
