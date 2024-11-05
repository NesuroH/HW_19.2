from django.db import models

# Create your models here.
from django.db import models


class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )
    slug = models.CharField(
        max_length=200,
        verbose_name="Slug",
        help_text="Введите slug"
    )
    content = models.TextField(
        verbose_name="Текст",
        help_text="Введите текст"
    )

    image = models.ImageField(
        upload_to="blog/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    views_count = models.IntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
