from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.checks import messages
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Version, Category


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for product in context_data['object_list']:
            active_version = Version.objects.filter(product=product, active=True).first()
            product.active_version = active_version
        return context_data


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    # fields = ("name", "description", "photo", "category", "price", "created_at", "updated_at", "manufactured_at")
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:menu')
    permission_required = (
        'catalog.can_change_product_status',
        'catalog.can_change_product_description',
        'catalog.can_change_product_category',)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.user:
            print(f'User: {self.request.user}, Permissions: {self.request.user.get_all_permissions()}')

            if not self.request.user.has_perms(self.permission_required):
                print('Permission denied: У пользователя нет необходимых разрешений')
                raise PermissionDenied

        return obj

    def has_permission(self):
        # Проверка прав для текущего пользователя
        return (
                self.request.user.has_perm('catalog.can_change_product_status') or
                self.request.user.has_perm('catalog.can_change_product_description') or
                self.request.user.has_perm('catalog.can_change_product_category') or
                self.request.user == self.get_object().user  # Позволить владельцу редактировать
        )

    def get_permission_object(self):
        return self.get_object()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы изменить продукт.')
            return redirect('users:login')

        if not self.has_permission():
            messages.error(request, 'У вас нет доступа к этой странице.')
            return redirect('catalog:menu')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ProductForm = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context["formset"] = ProductForm(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = ProductForm(instance=self.object)

        context['categories'] = Category.objects.all()
        context['title'] = 'Изменение карточки продукта'

        return context

    def get_form_class(self):
        user = self.request.user
        if self.object.user == user:
            return ProductForm
        if user.has_perm("catalog.can_change_product_status") and user.has_perm(
                "catalog.can_change_product_description") and user.has_perm(
            "catalog.can_change_product_category"):
            return ModeratorProductForm
        raise PermissionDenied

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        # Сохранение объекта
        self.object = form.save()
        # проверка валидности formset и сохраняем его
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ModeratorProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ModeratorProductForm
    template_name = 'catalog/moderator_product_form.html'
    success_url = reverse_lazy('catalog:menu')
    permission_required = (
        'catalog.can_change_product_status',
        'catalog.can_change_product_description',
        'catalog.can_change_product_category',
    )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')
