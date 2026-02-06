from rest_framework import serializers
from rest_framework.serializers import ValidationError

from adv.models import Advertisement, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""

    class Meta:
        model = Review
        fields = ("id", "author", "ad", "text")
        read_only_fields = (
            "id",
            "author",
        )

    def validate(self, data):
        data["author"] = self.context["request"].user
        if Review.objects.filter(**data).exists():
            raise ValidationError({"detail": "Такой объект уже существует"})
        return data


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели объявления"""

    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ("id", "title", "price", "description", "author", "reviews")
        read_only_fields = (
            "id",
            "author",
        )

    def validate(self, data):
        data["author"] = self.context["request"].user
        if Advertisement.objects.filter(**data).exists():
            raise ValidationError({"detail": "Такой объект уже существует"})
        return data
