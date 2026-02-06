from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from adv.models import Advertisement, Review
from adv.paginators import AdvertisementPaginator
from adv.permissions import IsOwner
from adv.serializers import AdvertisementSerializer, ReviewSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели объявления"""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("title",)
    pagination_class = AdvertisementPaginator

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [
                AllowAny,
            ]
        elif (
            self.action == "destroy"
            or self.action == "partial_update"
            or self.action == "update"
        ):
            self.permission_classes = [IsOwner | IsAdminUser]
        else:
            self.permission_classes = [
                IsAuthenticated,
            ]

        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзыва"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if (
            self.action == "destroy"
            or self.action == "partial_update"
            or self.action == "update"
        ):
            self.permission_classes = [IsOwner | IsAdminUser]
        else:
            self.permission_classes = [
                IsAuthenticated,
            ]

        return super().get_permissions()
