from rest_framework.pagination import PageNumberPagination


class AdvertisementPaginator(PageNumberPagination):
    """Пагинатор для объявлений"""

    page_size = 4
