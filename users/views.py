import json

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

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

    @swagger_auto_schema(
        operation_description="Отправка ссылки для сброса пароля пользователю",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email"),
            },
            required=["email"],
            example={"email": "test@test.com"},
        ),
        responses={
            200: openapi.Response(
                "",
                examples={
                    "application/json": {
                        "message": "Инструкция для сброса пароля отправлена на email"
                    }
                },
            )
        },
    )
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

    @swagger_auto_schema(
        operation_description="Сброс пароля по токену и уникальному идентификатору пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Новый пароль пользователя"
                ),
            },
            required=["new_password"],
            example={"new_password": "new_password_string"},
        ),
        responses={
            200: openapi.Response(
                "", examples={"application/json": {"message": "Пароль успешно изменен"}}
            )
        },
        manual_parameters=[
            openapi.Parameter(
                "uid",  # Имя параметра
                openapi.IN_QUERY,  # Местоположение параметра (в запросе)
                description="Персональный идентификатор пользователя",  # Описание параметра
                type=openapi.TYPE_INTEGER,  # Тип параметра (INTEGER, STRING и т.д.)
                required=True,  # Укажите, обязательный ли параметр
            ),
            openapi.Parameter(
                "token",  # Дополнительный параметр по поиску
                openapi.IN_QUERY,
                description="Токен пользователя для сброса пароля",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
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

                tokens = OutstandingToken.objects.filter(user=provided_user)
                for token in tokens:
                    BlacklistedToken.objects.create(token=token) # pragma: no cover

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
