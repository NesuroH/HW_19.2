from django.urls import path

from .apps import CatalogConfig
from .views import ProductListView, ProductDetailView

app_name = CatalogConfig.name



urlpatterns = [
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products_detail'),
]