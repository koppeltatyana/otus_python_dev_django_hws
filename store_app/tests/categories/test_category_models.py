import pytest
from store_app.models import Category


@pytest.mark.django_db
class TestCategoryModels:
    """Тесты на модели категории"""

    def test_category_creation(self, get_random_category_body, category_helpers):
        categories_count = category_helpers.get_categories_count()
        Category.objects.create(**get_random_category_body)
        new_categories_count = category_helpers.get_categories_count()
        assert categories_count + 1 == new_categories_count, (
            f"Количество категорий в БД не соответствует ожидаемому. "
            f"ОР: {categories_count + 1}, ФР: {new_categories_count}"
        )

    def test_category_creation_fields(self, create_category, category_helpers):
        category_helpers.should_be_category_in_list(category=create_category)

    def test_several_categories_creation(
        self, create_several_categories, category_helpers
    ):
        categories = create_several_categories()
        for category in categories:
            category_helpers.should_be_category_in_list(category)

    def test_category_update(self, create_category, category_helpers):
        categories_count = category_helpers.get_categories_count()
        new_category_data = {
            "name": "updated_" + create_category.name,
            "description": "updated_" + create_category.description,
        }
        new_category = Category(id=create_category.pk, **new_category_data)

        Category.objects.filter(id=create_category.pk).update(**new_category_data)
        category_helpers.should_be_category_in_list(new_category)

        new_categories_count = category_helpers.get_categories_count()
        assert categories_count == new_categories_count, (
            f"Количество категорий в БД изменилось после обновления категории. "
            f"ОР: {categories_count}, ФР: {new_categories_count}"
        )

    def test_category_delete(self, create_category, category_helpers):
        categories_count = category_helpers.get_categories_count()
        Category.objects.filter(id=create_category.pk).delete()

        new_categories_count = category_helpers.get_categories_count()
        assert categories_count - 1 == new_categories_count, (
            f"Количество категорий в БД не соответствует ожидаемому. "
            f"ОР: {categories_count - 1}, ФР: {new_categories_count}"
        )

    def test_category_invalid_delete(self, create_category, category_helpers):
        categories_count = category_helpers.get_categories_count()
        Category.objects.filter(id=create_category.pk * 10).delete()
        new_categories_count = category_helpers.get_categories_count()
        assert categories_count == new_categories_count, (
            f"Количество категорий в БД не соответствует ожидаемому. "
            f"ОР: {categories_count}, ФР: {new_categories_count}"
        )
