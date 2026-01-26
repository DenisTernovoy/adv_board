from django.db import models

from users.models import CustomUser


class Advertisement(models.Model):
    """Модель объявления"""

    title = models.CharField(max_length=50, verbose_name="Название")
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Автор"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.price}"


class Review(models.Model):
    """Модель отзыва"""

    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Автор"
    )
    ad = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, verbose_name="Объявление"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
