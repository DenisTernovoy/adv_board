from rest_framework import serializers

from users.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для контроллера на создание пользователя"""

    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "phone", "email", "password", "avatar")

    def create(self, validated_data) -> CustomUser:
        """Хэширование пароля"""

        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserResetPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для запроса на сброс пароля"""

    class Meta:
        model = CustomUser
        fields = ("email",)


class UserResetPasswordConfirmSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля"""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
