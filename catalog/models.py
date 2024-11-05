from django.db import models

from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    status = models.BooleanField(verbose_name='Статус продукта', default=False)
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание продукта"
    )
    photo = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену продукта")
    created_at = models.DateField(
        verbose_name="Дата создания", help_text="Введите дату создания продукта"
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения",
        help_text="Введите дату последнего изменения продукта",
        blank=True,
        null=True,
    )
    manufactured_at = models.DateField(
        verbose_name="Дата производства продукта",
        help_text="Введите дату производства продукта",
        blank=True,
        null=True,
    )
    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ('can_change_product_description', 'Может изменять описание продукта'),
            ('can_change_product_category', 'Может изменять категорию продукта'),
            ('can_change_product_status', 'Может изменять статус публикации продукта'),
        ]

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="versions",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Версия",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        null=True,
        blank=True,
        related_name="version_product",
    )

    version_num = models.PositiveIntegerField(
        verbose_name="Номер версии",
        help_text="Укажите номер версии продукта",
        default=0,
        null=True,
        blank=True,
    )

    version_name = models.CharField(
        max_length=100,
        verbose_name="Наименование версии",
        help_text="Введите наименование версии продукта",
        default="",
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        verbose_name="Признак текущей версии",
        help_text="Введите признак текущей версии продукта",
        default=False
    )

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продукта"
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
