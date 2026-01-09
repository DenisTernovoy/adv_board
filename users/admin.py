from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser
