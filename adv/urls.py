from adv.apps import AdvConfig
from rest_framework.routers import DefaultRouter
from adv.views import AdvertisementViewSet, ReviewViewSet

app_name = AdvConfig.name

router = DefaultRouter()
router.register(r"ads", AdvertisementViewSet, basename="advertisement")
router.register(r"reviews", ReviewViewSet, basename="reviews")

urlpatterns: list = []
urlpatterns += router.urls
