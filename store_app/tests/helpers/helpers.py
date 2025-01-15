import random
import string

from bs4 import BeautifulSoup
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from store_app.models import Category, Product


class CommonHelpers:
    """Класс для хранения общих доп методов"""

    @staticmethod
    def should_be_status_code(
        response: HttpResponse | TemplateResponse, expected_status_code: int
    ) -> None:
        """
        Проверка ответа на ожидаемый статус код

        :param response: Результат выполнения запроса
        :param expected_status_code: Ожидаемый статус код
        """
        assert (
            response.status_code == expected_status_code
        ), f"Статус код ответа {response.status_code} не соответствует ожидаемому {expected_status_code}"

    @staticmethod
    def should_be_redirect_url(
        response: HttpResponseRedirect, expected_response_url: str
    ) -> None:
        """
        Проверка url редиректа

        :param response: Результат выполнения запроса
        :param expected_response_url: Ожидаемый url
        """
        assert (
            response.url == expected_response_url
        ), f"URL редиректа {response.url} не соответствует ожидаемому {expected_response_url}"

    @staticmethod
    def get_random_str(str_len: int = 10) -> str:
        """
        Получение случайной строки

        :param str_len: Длина строки
        :return: Сгенерированная строка
        """
        characters = (
            string.ascii_letters + string.digits
        )  # Включает буквы (верхний и нижний регистры) и цифры
        random_string = "".join(random.choice(characters) for _ in range(str_len))
        return random_string

    @staticmethod
    def get_text_list_from_html_by_tag(
        decoded_response: str, tag_name: str
    ) -> list[str]:
        """
        Получение списка текстов со страницы по тегу

        :param decoded_response: Декодированный ответ на запрос в виде html
        :param tag_name: Наименование тега
        :return: Список найденных по тегу элементов
        """
        soup = BeautifulSoup(decoded_response, "html.parser")
        elements = soup.find_all(tag_name)
        assert elements, f"На странице нет элементов с тегом {tag_name}"
        return [x.text for x in elements]

    def should_be_text_by_tag_on_page(
        self, decoded_response: str, tag_name: str, expected_text: str
    ) -> None:
        """
        Проверить наличие текста на странице по тегу

        :param decoded_response: Декодированный ответ на запрос в виде html
        :param tag_name: Наименование тега
        :param expected_text: Ожидаемый текст
        """
        text_elements = self.get_text_list_from_html_by_tag(decoded_response, tag_name)
        for element in text_elements:
            if expected_text in element:
                return
        raise AssertionError(
            f"Текста {expected_text} по тегу {tag_name} нет на странице"
        )

    @staticmethod
    def get_random_float(
        min_val: int | float = 10.0, max_val: int | float = 100.0
    ) -> float:
        """
        Генерация случайного числа с плавающей точкой в указанном диапазоне

        :param min_val: Левая граница диапазона
        :param max_val: Правая граница диапазона
        """
        return round(random.uniform(min_val, max_val), 2)


class ProductHelpers:
    """Класс для хранения доп методов для продукта"""

    @staticmethod
    def get_product_list() -> list[Product]:
        """Получить список продуктов"""
        return Product.objects.all()

    @staticmethod
    def get_products_count() -> int:
        """Получить количество продуктов"""
        return Product.objects.count()

    @staticmethod
    def should_be_product_in_list(product: Product) -> None:
        """
        Проверка наличия продукта в общем списке продуктов

        :param product: Проверяемый продукт
        """
        assert Product.objects.filter(
            id=product.pk,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category.id,
        ), f"Продукта {product} нет в общем списке продуктов"


class CategoryHelpers:
    """Класс для хранения доп методов для категории"""

    @staticmethod
    def get_category_list() -> list[Category]:
        """Получить список категорий"""
        return Category.objects.all()

    @staticmethod
    def should_be_category_in_list(category: Category):
        """
        Проверка наличия категории в общем списке категорий

        :param category: Проверяемая категория
        """
        assert Category.objects.filter(
            id=category.pk,
            name=category.name,
            description=category.description,
        ), f"Категории {category} нет в списке категорий"

    @staticmethod
    def get_categories_count() -> int:
        """Получить количество категорий"""
        return Category.objects.count()
