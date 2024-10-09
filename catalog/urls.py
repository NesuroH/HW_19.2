
from catalog.views import HomePageView, ContactsView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

from django.urls import path
from catalog.apps import CatalogConfig


app_name = CatalogConfig.name


urlpatterns = [
    path('home', HomePageView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('catalog/', ProductListView.as_view(), name='product_list'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]