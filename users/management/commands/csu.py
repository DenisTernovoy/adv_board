from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    """Команда для создания суперпользователя"""

    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            first_name="Администратор DJANGO",
            email="admin@admin.com",
        )
        user.set_password("12345")
        user.is_staff = True
        user.is_superuser = True
        user.role = "admin"

        user.save()
