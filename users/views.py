from rest_framework import generics

from users.models import CustomUser
from users.serializers import UserCreateSerializer


class CreateUser(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
