from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомный класс пользователя"""

    username = None

    first_name = models.CharField(max_length=50, help_text="Имя", verbose_name="Имя")
    last_name = models.CharField(
        max_length=50, help_text="Фамилия", verbose_name="Фамилия"
    )
    phone = models.CharField(max_length=25, help_text="Телефон", verbose_name="Телефон")
    email = models.EmailField(unique=True, help_text="Email", verbose_name="Email")
    role = models.CharField(default="user", help_text="Роль", verbose_name="Роль")

    # Поле "Аватар" с потенциалом на frontend
    avatar = models.ImageField(
        null=True, blank=True, help_text="Аватар", verbose_name="Аватар"
    )

    # Технические поля
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-created_at"]
