from django.urls import include, path
from rest_framework.routers import DefaultRouter

from adv.apps import AdvConfig
from adv.views import AdvertisementViewSet, ReviewViewSet

app_name = AdvConfig.name

router_adv = DefaultRouter()
router_adv.register(r"", AdvertisementViewSet, basename="advertisement")


router_review = DefaultRouter()
router_review.register(r"", ReviewViewSet, basename="reviews")

urlpatterns: list = [
    path("ads/<int:ad_pk>/reviews/", include(router_review.urls), name="reviews"),
    path("ads/", include(router_adv.urls), name="advertisement"),
]

urlpatterns += router_adv.urls
