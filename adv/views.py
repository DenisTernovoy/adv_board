from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from adv.models import Advertisement, Review
from adv.serializers import AdvertisementSerializer, ReviewSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели объявления"""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except Exception:
            raise ValidationError({"detail": "Такой объект уже существует."})


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзыва"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except Exception:
            raise ValidationError({"detail": "Данный отзыв уже был оставлен Вами."})
