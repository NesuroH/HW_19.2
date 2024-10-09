from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.CharField(
        max_length=200, verbose_name="Описание", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="catalog/photo",
        blank=True,
        null=True,
        verbose_name="фото",
        help_text="Загрузите фото продукта",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        blank=True,
        null=True,
        related_name="catalog",
    )
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену продукта")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name", "price", "category", "created_at", "updated_at"]


class Category(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Имя", help_text="Введите название"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="продукт",
    )
    version_number = models.CharField(
        max_length=200, verbose_name="Номер версии", help_text="Введите номер версии"
    )
    version_name = models.CharField(
        max_length=200,
        verbose_name="Название версии",
        help_text="Введите название версии",
    )
    sign = models.BooleanField(
        verbose_name="Признак текущей версии"
    )

    def __str__(self):
        return self.version_name

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"
        ordering = ["product", "version_number", "version_name", "sign"]