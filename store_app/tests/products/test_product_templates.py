import pytest
from django.urls import reverse_lazy
from store_app.models import Product


class TestProductTemplates:
    """Тесты на шаблоны продукта"""

    @pytest.mark.django_db
    def test_product_list_template(
        self, create_product: Product, client, common_helpers
    ):
        response = client.get(path=reverse_lazy("product_list"))
        assert (
            response.status_code == 200
        ), f"Статус код не соответствует ожидаемому. ОР: 200, ФР: {response.status_code}"
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h4",
            expected_text=create_product.name,
        )

    @pytest.mark.django_db
    def test_product_create_template(self, client, common_helpers):
        response = client.get(path=reverse_lazy("product_create"))
        assert (
            response.status_code == 200
        ), f"Статус код не соответствует ожидаемому. ОР: 200, ФР: {response.status_code}"
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text="Добавление продукта",
        )

    @pytest.mark.django_db
    def test_product_detail_template(
        self, create_product: Product, client, common_helpers
    ):
        response = client.get(
            path=reverse_lazy("product_detail", args=[create_product.pk])
        )
        assert (
            response.status_code == 200
        ), f"Статус код не соответствует ожидаемому. ОР: 200, ФР: {response.status_code}"
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text=create_product.name,
        )

    @pytest.mark.django_db
    def test_product_edit_template(
        self, create_product: Product, client, common_helpers
    ):
        response = client.get(
            path=reverse_lazy("product_edit", args=[create_product.pk])
        )
        assert (
            response.status_code == 200
        ), f"Статус код не соответствует ожидаемому. ОР: 200, ФР: {response.status_code}"
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text="Редактирование продукта",
        )

    @pytest.mark.django_db
    def test_product_delete_template(
        self, create_product: Product, client, common_helpers
    ):
        response = client.get(
            path=reverse_lazy("product_delete", args=[create_product.pk])
        )
        assert (
            response.status_code == 200
        ), f"Статус код не соответствует ожидаемому. ОР: 200, ФР: {response.status_code}"
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text=f"Вы точно хотите удалить продукт {create_product.name}?",
        )
