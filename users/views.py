import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import generics, status, views
from rest_framework.response import Response

from config import settings
from users.models import CustomUser
from users.serializers import (
    UserCreateSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
)
from users.tasks import send_message

token_generator = PasswordResetTokenGenerator()


class CreateUser(generics.CreateAPIView):
    """Регистрация пользователя"""

    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer


class UserResetPassword(views.APIView):
    """Отправка ссылки для сброса пароля пользователю"""

    def post(self, request, *args, **kwargs):  # noqa

        serializer = UserResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provided_user = CustomUser.objects.filter(
            email=serializer.validated_data["email"]
        ).first()

        if provided_user:
            token = token_generator.make_token(provided_user)
            provided_user.token = token
            provided_user.save()

            uid = provided_user.pk
            reset_link = f"{settings.BASE_URL}/users/reset_password_confirm?uid={uid}&token={token}"
            subject = "Сброс пароля"

            data = {"new_password": "P4$$W0RD"}
            message = f"""Для сброса пароля отправьте POST запрос с новым паролем по ссылке: {reset_link}

                        Форма запроса:
                        {json.dumps(data, indent=4)}
                """

            print(message)

            send_message.delay(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [
                    provided_user.email,
                ],
            )

            return Response(
                {"message": "Инструкция для сброса пароля отправлена на email"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Пользователя с таким email не существует"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserResetPasswordConfirm(views.APIView):
    """Сброс пароля по токену и уникальному идентификатору пользователя"""

    def post(self, request, *args, **kwargs):  # noqa
        provided_user = CustomUser.objects.filter(
            pk=request.query_params["uid"]
        ).first()

        serializer = UserResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if provided_user:
            if provided_user.token == request.query_params["token"]:
                provided_user.set_password(serializer.validated_data["new_password"])
                provided_user.token = token_generator.make_token(provided_user)
                provided_user.save()
                return Response({"message": "Пароль успешно изменен"})
            else:
                return Response(
                    {"detail": "Неверный token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"detail": "Пользователя с таким uid не существует"},
                status=status.HTTP_400_BAD_REQUEST,
            )
