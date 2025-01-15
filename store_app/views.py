from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Category, Product
from .forms import CategoryModelForm, ProductModelForm
from .tasks import ActionName, updated_category, updated_product


def index(request):
    return render(request, template_name="store_app/home.html")


class ProductView:
    """Базовый класс для модели Product"""

    model = Product


class ProductListView(ProductView, ListView):
    """Представление для отображения списка продуктов"""

    template_name = "store_app/product_list.html"
    context_object_name = "products"
    paginate_by = 5


class ProductDetailView(ProductView, DetailView):
    """Представление для отображения деталей продукта"""

    template_name = "store_app/product_detail.html"
    context_object_name = "product"


class ProductCreateView(ProductView, CreateView):
    """Представление для отображения страницы создания продукта"""

    template_name = "store_app/product_create.html"
    form_class = ProductModelForm
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        updated_product.delay(
            action_name=ActionName.created, product_name=form.instance.name
        )
        messages.success(
            self.request, f'Продукт "{form.instance.name}" успешно создан!'
        )
        return response


class ProductUpdateView(ProductView, UpdateView):
    """Представление для редактирования продукта"""

    template_name = "store_app/product_edit.html"
    form_class = ProductModelForm
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        updated_product.delay(
            action_name=ActionName.updated, product_name=form.instance.name
        )
        messages.success(
            self.request, f'Продукт "{form.instance.name}" успешно изменен!'
        )
        return response


class ProductDeleteView(ProductView, DeleteView):
    """Представление для удаления продукта"""

    template_name = "store_app/product_delete.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        updated_product.delay(
            action_name=ActionName.deleted, product_name=self.object.name
        )
        messages.info(self.request, f'Продукт "{self.object.name}" успешно удален!')
        return response


class CategoryView:
    """Базовый класс для представления модели Category"""

    model = Category


class CategoryListView(CategoryView, ListView):
    """Представление для отображения списка продуктов"""

    template_name = "store_app/category_list.html"
    context_object_name = "categories"
    paginate_by = 5


class CategoryDetailView(CategoryView, DetailView):
    """Представление для отображения деталей категории"""

    template_name = "store_app/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        """Переопределить объект контекста"""
        context = super().get_context_data(**kwargs)
        context["category_products"] = Product.objects.filter(
            category=self.object
        ).order_by("id")
        return context


class CategoryCreateView(CategoryView, CreateView):
    """Представление для отображения страницы создания категории"""

    template_name = "store_app/category_create.html"
    form_class = CategoryModelForm
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        updated_category.delay(
            action_name=ActionName.created, category_name=form.instance.name
        )
        messages.success(
            self.request, f'Категория "{form.instance.name}" успешно создана!'
        )
        return response


class CategoryUpdateView(CategoryView, UpdateView):
    """Представление для редактирования категории"""

    template_name = "store_app/category_edit.html"
    form_class = CategoryModelForm
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        updated_category.delay(
            action_name=ActionName.updated, category_name=form.instance.name
        )
        messages.success(
            self.request, f'Категория "{form.instance.name}" успешно изменена!'
        )
        return response


class CategoryDeleteView(CategoryView, DeleteView):
    """Представление для удаления категории"""

    template_name = "store_app/category_delete.html"
    success_url = reverse_lazy("category_list")

    def get_context_data(self, **kwargs):
        """Переопределить объект контекста"""
        context = super().get_context_data(**kwargs)
        context["category_products"] = Product.objects.filter(
            category=self.object
        ).order_by("id")
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        updated_category.delay(
            action_name=ActionName.deleted, category_name=self.object.name
        )
        messages.info(self.request, f'Категория "{self.object.name}" успешно удалена!')
        return response
