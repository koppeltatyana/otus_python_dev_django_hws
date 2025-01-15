import pytest
from faker import Faker

from ..models import Category, Product
from store_app.tests.helpers.helpers import (
    CategoryHelpers,
    ProductHelpers,
    CommonHelpers,
)


@pytest.fixture(scope="session")
def common_helpers() -> CommonHelpers:
    """Клиент CommonHelpers"""
    return CommonHelpers()


@pytest.fixture(scope="session")
def product_helpers() -> ProductHelpers:
    """Клиент ProductHelpers"""
    return ProductHelpers()


@pytest.fixture(scope="session")
def category_helpers() -> CategoryHelpers:
    """Клиент CategoryHelpers"""
    return CategoryHelpers()


@pytest.fixture(scope="session")
def fake() -> Faker:
    """Клиент Faker"""
    return Faker()


@pytest.fixture
def get_random_category_body(fake):
    return {
        "name": CommonHelpers.get_random_str(),
        "description": fake.sentence(),
    }


@pytest.fixture
def create_category(get_random_category_body) -> Category:
    """Создание категории"""
    return Category.objects.create(**get_random_category_body)


@pytest.fixture
def create_several_categories(fake):
    """Создание нескольких категорий"""

    def wrapper(categories_count: int = 3) -> list[Category]:
        """
        :param categories_count: Необходимое количество категорий
        """
        categories = []
        for _ in range(categories_count):
            categories += [
                Category.objects.create(
                    name=CommonHelpers.get_random_str(),
                    description=fake.sentence(),
                )
            ]
        return categories

    return wrapper


@pytest.fixture
def get_random_product_body(fake, create_category) -> dict:
    return {
        "name": CommonHelpers.get_random_str(),
        "description": fake.sentence(),
        "price": CommonHelpers.get_random_float(),
        "category": create_category,
    }


@pytest.fixture
def create_product(fake: Faker, get_random_product_body: dict) -> Product:
    """Создание продукта"""
    return Product.objects.create(**get_random_product_body)


@pytest.fixture
def create_several_products(fake, create_category):
    """Создание нескольких категорий"""

    def wrapper(products_count: int = 3) -> list[Product]:
        """
        :param products_count: Необходимое количество продуктов
        """
        products = []
        for _ in range(products_count):
            products += [
                Product.objects.create(
                    name=fake.word().capitalize(),
                    description=fake.sentence(),
                    price=CommonHelpers.get_random_float(),
                    category=create_category,
                )
            ]
        return products

    return wrapper
