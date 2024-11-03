from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField
from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ("views_counter", "owner")

    lock_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    def clean_name(self):
        product_name = self.cleaned_data["name"]
        name_list = product_name.split()
        for part_name in name_list:
            for part_name in self.lock_words:
                if part_name.lower() in product_name.lower():
                    raise ValidationError(f"В названии продукта не должно быть слова '{part_name}' ")

        return product_name

    def clean_description(self):
        description = self.cleaned_data["description"]
        description_list = description.split()
        for part_description in description_list:
            for part_description in self.lock_words:
                if part_description.lower() in description.lower():
                    raise ValidationError(f"В описании продукта не должно быть слова '{part_description}' ")

        return description

class ModeratorProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'status')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'



class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
        # exclude = ("views_counter",)

    """def clean_active(self):
        product = self.instance  # продукт, с которым работаем
        versions = product.version_set.all()  # все версии продукта
        cleaned_data = self.cleaned_data["active"]

        if versions.filter(is_active=True).exists() and cleaned_data:
            raise ValidationError('Не может быть несколько актуальных версий')

        return cleaned_data"""