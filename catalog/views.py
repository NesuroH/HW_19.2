from .models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products_detail.html'
    context_object_name = 'product'

