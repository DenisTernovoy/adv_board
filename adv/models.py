from django.db import models

from users.models import CustomUser


class Advertisement(models.Model):
    """Модель объявления"""

    title = models.CharField(max_length=50, verbose_name="Название")
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "price", "author", "description"],
                name="unique_advertisement",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.price}"


class Review(models.Model):
    """Модель отзыва"""

    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        null=True,
        blank=True,
        related_name="author",
    )
    ad = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        verbose_name="Объявление",
        related_name="reviews",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "ad", "text"], name="unique_review"
            ),
        ]

    def __str__(self):
        return self.text
