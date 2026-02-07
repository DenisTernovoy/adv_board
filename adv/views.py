from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

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

    def create(self, request, ad_pk=None):
        data = request.data.copy()
        data["ad"] = ad_pk

        serializer = ReviewSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, ad_pk=None, pk=None, **kwargs):
        partial = kwargs.pop("partial", False)  # Позволяет частичное обновление
        data = request.data.copy()
        data["ad"] = ad_pk
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)

        if serializer.is_valid():
            # Дополнительная логика перед сохранением
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        ad = self.kwargs["ad_pk"]
        queryset = Review.objects.filter(ad=ad)
        return queryset

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
