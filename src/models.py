import json
from abc import ABC, abstractmethod
from typing import List


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def some_abstract_method(self):
        """Абстрактный метод, чтобы класс был действительно абстрактным."""
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_dict):
        """Создать новый продукт из словаря."""
        pass


class CreationInfoMixin:
    """
    Миксин, который при создании объекта
    выводит информацию о классе и параметрах,
    а также реализует __repr__.
    """

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        print(f"Создан объект класса {class_name} "
              f"с параметрами: args={args}, kwargs={kwargs}")
        # Не вызываем super().__init__, чтобы избежать ошибки

    def __repr__(self):
        params = []
        for attr in ('name', 'description', 'price', 'quantity'):
            value = getattr(self, attr, None)
            if value is not None:
                params.append(f"{attr}={value!r}")
        params_str = ", ".join(params)
        return f"{self.__class__.__name__}({params_str})"


class Product(CreationInfoMixin, BaseProduct):
    """
    Базовый класс для описания товара.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.__price = None
        # Явно вызываем миксин, чтобы вывести информацию
        CreationInfoMixin.__init__(self, name, description, price, quantity)
        # Инициализируем атрибуты
        self.name = name
        self.description = description
        self.price = price  # через сеттер с проверкой
        self.quantity = quantity

    def some_abstract_method(self):
        """Реализация абстрактного метода из BaseProduct."""
        pass

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
        # Универсальный конструктор для наследников
        return cls(**product_dict)

    def __str__(self):
        return f"{self.name}, {int(self.price)} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return CreationInfoMixin.__repr__(self)

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного типа")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    def __init__(self, name, description, price,
                 quantity, efficiency, model, memory, color):
        # Вызываем Product.__init__ напрямую
        Product.__init__(self, name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self):
        base_repr = CreationInfoMixin.__repr__(self)
        return (f"{base_repr[:-1]}, "
                f"efficiency={self.efficiency!r}, model={self.model!r}, "
                f"memory={self.memory!r}, color={self.color!r})")


class LawnGrass(Product):
    def __init__(self, name, description, price,
                 quantity, country, germination_period, color):
        Product.__init__(self, name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self):
        base_repr = CreationInfoMixin.__repr__(self)
        return (f"{base_repr[:-1]}, country={self.country!r}, "
                f"germination_period={self.germination_period!r}, "
                f"color={self.color!r})")


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
            raise TypeError("Можно добавлять "
                            "только объекты Product или его наследников")
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

    def middle_price(self) -> float:
        try:
            total_price = sum(p.price for p in self.__products)
            count = len(self.__products)
            return total_price / count
        except ZeroDivisionError:
            return 0


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
