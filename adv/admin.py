from django.contrib import admin

from adv.models import Advertisement, Review


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "description", "author", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "ad", "created_at")
