from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "product_detail/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path("product_create/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "product_edit/<int:pk>/", views.ProductUpdateView.as_view(), name="product_edit"
    ),
    path(
        "product_delete/<int:pk>/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path(
        "category_detail/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "category_create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category_edit/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="category_edit",
    ),
    path(
        "category_delete/<int:pk>/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
