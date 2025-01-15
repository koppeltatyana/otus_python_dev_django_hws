import pytest
from store_app.forms import ProductModelForm
from store_app.tests.helpers.helpers import CommonHelpers


@pytest.mark.django_db
class TestProductForms:
    """Тесты на формы продукта"""

    @pytest.mark.parametrize(
        "name, description, price, is_valid",
        [
            ("Тестовый продукт", "Описание продукта", 10, True),
            ("Тестовый продукт", "Описание продукта", 0, False),
            ("Тестовый продукт", "Описание продукта", -1, False),
            (CommonHelpers.get_random_str(str_len=2), "Описание продукта", 0.5, False),
            (CommonHelpers.get_random_str(str_len=3), "Описание продукта", 100, True),
            (CommonHelpers.get_random_str(str_len=26), "Описание категории", 15, False),
            (CommonHelpers.get_random_str(str_len=25), "Описание категории", 20, True),
            ("Тестовый продукт", "", 100, True),
            (
                "Тестовый продукт",
                CommonHelpers.get_random_str(str_len=100),
                100,
                True,
            ),
            (
                "Тестовый продукт",
                CommonHelpers.get_random_str(str_len=101),
                100,
                False,
            ),
            ("Тестовый продукт", None, 1, True),
            ("Тестовый продукт", None, -1, False),
            (None, None, 0, False),
        ],
    )
    def test_product_form(self, name, description, price, is_valid, create_category):
        form_data = {
            "name": name,
            "description": description,
            "price": price,
            "category": create_category,
        }
        form = ProductModelForm(data=form_data)
        assert form.is_valid() is is_valid, (
            f"Валидность формы с данными {form_data} не соответствует ожидаемому значению. "
            f"ОР: {is_valid}, ФР: {form.is_valid()}"
        )
