from rest_framework import serializers

from adv.models import Advertisement, Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзыва"""

    class Meta:
        model = Review
        fields = (
            "text",
            "ad",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыва"""

    author_name = serializers.CharField(source="author", read_only=True)
    ad = serializers.SerializerMethodField()

    def get_ad(self, obj):
        return str(obj.ad)

    class Meta:
        model = Review
        fields = ("id", "author_name", "ad", "text")


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели объявления"""

    author_name = serializers.CharField(source="author", read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = ("id", "title", "price", "description", "author_name", "reviews")
