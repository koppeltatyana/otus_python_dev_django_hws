import pytest
from store_app.forms import CategoryModelForm
from store_app.tests.helpers.helpers import CommonHelpers


@pytest.mark.django_db
class TestCategoryForms:
    """Тесты на формы категории"""

    @pytest.mark.parametrize(
        "name, description, is_valid",
        [
            ("Тестовая категория", "Описание категории", True),
            (CommonHelpers.get_random_str(str_len=2), "Описание категории", False),
            (CommonHelpers.get_random_str(str_len=3), "Описание категории", True),
            (CommonHelpers.get_random_str(str_len=26), "Описание категории", False),
            (CommonHelpers.get_random_str(str_len=25), "Описание категории", True),
            ("Тестовая категория", "", True),
            ("Тестовая категория", CommonHelpers.get_random_str(str_len=100), True),
            ("Тестовая категория", CommonHelpers.get_random_str(str_len=101), False),
            ("Тестовая категория", None, True),
            (None, None, False),
        ],
    )
    def test_category_form(self, name, description, is_valid):
        form_data = {"name": name, "description": description}
        form = CategoryModelForm(data=form_data)
        assert (
            form.is_valid() == is_valid
        ), f"Валидность формы не соответствует ожидаемому значению. ОР: {is_valid}, ФР: {form.is_valid()}"
