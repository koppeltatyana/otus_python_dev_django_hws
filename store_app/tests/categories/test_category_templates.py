import pytest
from django.urls import reverse_lazy
from store_app.models import Category


class TestCategoryTemplates:
    """Тесты на шаблоны категории"""

    @pytest.mark.django_db
    def test_category_list_template(
        self, create_category: Category, client, common_helpers
    ):
        response = client.get(path=reverse_lazy("category_list"))
        common_helpers.should_be_status_code(response, 200)
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h4",
            expected_text=create_category.name,
        )

    @pytest.mark.django_db
    def test_category_create_template(self, client, common_helpers):
        response = client.get(path=reverse_lazy("category_create"))
        common_helpers.should_be_status_code(response, 200)
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text="Добавление категории",
        )

    @pytest.mark.django_db
    def test_category_detail_template(
        self, create_category: Category, client, common_helpers
    ):
        response = client.get(
            path=reverse_lazy("category_detail", args=[create_category.pk])
        )
        common_helpers.should_be_status_code(response, 200)
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text=create_category.name,
        )

    @pytest.mark.django_db
    def test_category_edit_template(
        self, create_category: Category, client, common_helpers
    ):
        response = client.get(
            path=reverse_lazy("category_edit", args=[create_category.pk])
        )
        common_helpers.should_be_status_code(response, 200)
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text="Редактирование категории",
        )

    @pytest.mark.django_db
    def test_category_delete_template(
        self, create_category: Category, client, common_helpers
    ):
        response = client.get(
            path=reverse_lazy("category_delete", args=[create_category.pk])
        )
        common_helpers.should_be_status_code(response, 200)
        common_helpers.should_be_text_by_tag_on_page(
            decoded_response=response.content.decode(),
            tag_name="h1",
            expected_text=f"Вы точно хотите удалить категорию {create_category.name}?",
        )
