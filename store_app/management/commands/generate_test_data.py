from store_app.models import Category, Product
from django.core.management.base import BaseCommand
import random
from faker import Faker


class Command(BaseCommand):
    help = "Генерация тестовых данных (категорий и товаров)"

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories_count = 5
        products_count_per_category = 5 * categories_count

        self.stdout.write(f"Начало генерации {categories_count} категорий")
        categories = []
        for _ in range(categories_count):
            category_description = fake.sentence(nb_words=10)
            category = Category.objects.create(
                name=fake.word().capitalize(),
                description=(
                    category_description
                    if len(category_description) < 100
                    else category_description[:97] + "..."
                ),
            )
            categories += [category]
        self.stdout.write(f"Завершена генерация {categories_count} категорий")

        self.stdout.write(f"Начало генерации {products_count_per_category} продуктов")
        for _ in range(products_count_per_category):
            product_description = fake.sentence(nb_words=10)
            Product.objects.create(
                name=fake.word().capitalize(),
                description=(
                    product_description
                    if len(product_description) < 100
                    else product_description[:97] + "..."
                ),
                price=round(random.uniform(1, 100), 2),
                category=random.choice(categories),
            )
        self.stdout.write(
            f"Завершена генерация {products_count_per_category} продуктов"
        )
