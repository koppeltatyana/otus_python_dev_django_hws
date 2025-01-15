import pytest
from django.urls import reverse_lazy


def test_index(client, common_helpers):
    response = client.get(path=reverse_lazy("index"))
    common_helpers.should_be_status_code(response, 200)
    common_helpers.should_be_text_by_tag_on_page(
        decoded_response=response.content.decode(),
        tag_name="h1",
        expected_text="Добро пожаловать!",
    )


@pytest.mark.django_db
class TestCategoryViews:
    """Тесты на вьюшки категории"""

    def test_category_list_view(
        self, client, create_several_categories, common_helpers
    ):
        created_categories = [
            x.name for x in create_several_categories(categories_count=5)
        ]
        response = client.get(path=reverse_lazy("category_list"), data={"page": "1"})

        categories_from_ui = common_helpers.get_text_list_from_html_by_tag(
            decoded_response=response.content.decode(),
            tag_name="h4",
        )
        assert categories_from_ui == created_categories, (
            "Наименования созданных категорий не соответствует наименованиям категорий с UI. "
            f"ОР: {created_categories}. ФР: {categories_from_ui}"
        )

    def test_category_detail_view(self, client, create_category, common_helpers):
        response = client.get(
            path=reverse_lazy("category_detail", args=[create_category.pk])
        )
        category_names_from_ui = common_helpers.get_text_list_from_html_by_tag(
            decoded_response=response.content.decode(),
            tag_name="h1",
        )
        assert (
            len(category_names_from_ui) == 1
        ), "На странице больше одного заголовка первого уровня"
        category_name_from_ui = category_names_from_ui[0]
        created_category_name = f'Категория "{create_category.name}"'
        assert category_name_from_ui == created_category_name, (
            "Наименование созданной категории не соответствует наименованию категории с UI. "
            f"ОР: {created_category_name}, ФР: {category_name_from_ui}"
        )

    def test_category_create_view(
        self, client, get_random_category_body, common_helpers
    ):
        response = client.post(
            reverse_lazy("category_create"),
            data=get_random_category_body,
            format="json",
        )
        common_helpers.should_be_status_code(response, 302)
        common_helpers.should_be_redirect_url(response, "/categories/")

    def test_category_update_view(self, client, create_category, common_helpers):
        data = {
            "name": "updated_" + create_category.name,
            "description": "update_" + create_category.description,
        }
        response = client.post(
            reverse_lazy("category_edit", args=[create_category.pk]),
            data=data,
            format="json",
        )
        common_helpers.should_be_status_code(response, 302)
        common_helpers.should_be_redirect_url(response, "/categories/")

    def test_category_delete_view(self, client, create_category, common_helpers):
        response = client.post(
            reverse_lazy("category_delete", args=[create_category.pk])
        )
        common_helpers.should_be_status_code(response, 302)
        common_helpers.should_be_redirect_url(response, "/categories/")
