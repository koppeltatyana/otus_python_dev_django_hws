import pytest
from django.urls import reverse_lazy


@pytest.mark.django_db
class TestProductViews:
    """Тесты на вьюшки продукта"""

    def test_product_list_view(self, client, create_several_products, common_helpers):
        created_products = [x.name for x in create_several_products(products_count=5)]
        response = client.get(path=reverse_lazy("product_list"), data={"page": "1"})

        products_from_ui = common_helpers.get_text_list_from_html_by_tag(
            decoded_response=response.content.decode(),
            tag_name="h4",
        )
        assert products_from_ui == created_products, (
            "Наименования созданных продуктов не соответствует наименованиям продуктов с UI. "
            f"ОР: {created_products}. ФР: {products_from_ui}"
        )

    def test_product_detail_view(self, client, create_product, common_helpers):
        response = client.get(
            path=reverse_lazy("product_detail", args=[create_product.pk])
        )
        product_names_from_ui = common_helpers.get_text_list_from_html_by_tag(
            decoded_response=response.content.decode(),
            tag_name="h1",
        )
        assert (
            len(product_names_from_ui) == 1
        ), "На странице больше одного заголовка первого уровня"
        product_name_from_ui = product_names_from_ui[0]
        created_product_name = f'Продукт "{create_product.name}"'
        assert product_name_from_ui == created_product_name, (
            "Наименование созданного продукта не соответствует наименованию продукта с UI. "
            f"ОР: {created_product_name}, ФР: {product_name_from_ui}"
        )

    def test_product_create_view(self, client, get_random_product_body, common_helpers):
        response = client.post(
            reverse_lazy("product_create"),
            data={
                **get_random_product_body,
                "category": get_random_product_body.get("category").pk,
            },
            format="json",
        )
        common_helpers.should_be_status_code(response, 302)
        common_helpers.should_be_redirect_url(response, "/products/")

    def test_product_update_view(self, client, create_product, common_helpers):
        data = {
            "name": "updated_" + create_product.name,
            "description": "update_" + create_product.description,
            "price": common_helpers.get_random_float(),
            "category": create_product.category.pk,
        }
        response = client.post(
            reverse_lazy("product_edit", args=[create_product.pk]),
            data=data,
            format="json",
        )
        common_helpers.should_be_status_code(response, 302)
        common_helpers.should_be_redirect_url(response, "/products/")

    def test_product_delete_view(self, client, create_product, common_helpers):
        response = client.post(reverse_lazy("product_delete", args=[create_product.pk]))
        common_helpers.should_be_status_code(response, 302)
        common_helpers.should_be_redirect_url(response, "/products/")
