from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание категории', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Продукт')
    description = models.TextField(verbose_name='Описание продукта', null=True, blank=True)
    image = models.ImageField(upload_to='catalog/images', verbose_name="Изображение", blank=True, null=True, )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', related_name='products', blank=True, null=True)
    price = models.IntegerField(verbose_name="Цена")
    created_at = models.DateField(verbose_name='Дата добавления')
    updated_at = models.DateTimeField(verbose_name='Последний раз редактировано')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name



