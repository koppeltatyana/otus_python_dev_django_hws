import pytest
from store_app.models import Product
from store_app.tests.helpers.helpers import CommonHelpers


@pytest.mark.django_db
class TestProductModels:
    """Тесты на модели продукта"""

    def test_product_creation(self, fake, get_random_product_body, product_helpers):
        products_count = product_helpers.get_products_count()
        Product.objects.create(**get_random_product_body)
        new_products_count = product_helpers.get_products_count()
        assert products_count + 1 == new_products_count, (
            f"Количество продуктов в БД не соответствует ожидаемому. "
            f"ОР: {products_count + 1}, ФР: {new_products_count}"
        )

    def test_product_creation_fields(self, create_product, product_helpers):
        product_helpers.should_be_product_in_list(product=create_product)

    def test_several_products_creation(self, create_several_products, product_helpers):
        products = create_several_products()
        for product in products:
            product_helpers.should_be_product_in_list(product)

    def test_product_update(self, create_product, fake, product_helpers):
        products_count = product_helpers.get_products_count()
        new_product_data = {
            "name": "updated_" + create_product.name,
            "description": "updated_" + create_product.description,
            "price": CommonHelpers.get_random_float(),
            "category": create_product.category,
        }
        new_product = Product(id=create_product.pk, **new_product_data)

        Product.objects.filter(id=create_product.pk).update(**new_product_data)
        product_helpers.should_be_product_in_list(new_product)

        new_products_count = product_helpers.get_products_count()
        assert products_count == new_products_count, (
            f"Количество категорий в БД изменилось после обновления категории. "
            f"ОР: {products_count}, ФР: {new_products_count}"
        )

    def test_product_delete(self, create_product, product_helpers):
        products_count = product_helpers.get_products_count()
        Product.objects.filter(id=create_product.pk).delete()

        new_products_count = product_helpers.get_products_count()
        assert products_count - 1 == new_products_count, (
            f"Количество продуктов в БД не соответствует ожидаемому. "
            f"ОР: {products_count - 1}, ФР: {new_products_count}"
        )

    def test_product_invalid_delete(self, create_product, product_helpers):
        products_count = product_helpers.get_products_count()
        Product.objects.filter(id=create_product.pk * 10).delete()
        new_products_count = product_helpers.get_products_count()
        assert products_count == new_products_count, (
            f"Количество продуктов в БД не соответствует ожидаемому. "
            f"ОР: {products_count}, ФР: {new_products_count}"
        )
