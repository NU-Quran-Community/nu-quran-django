from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "name_ar", "value")
    search_fields = ("name",)


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "date")
    list_filter = ("category", "date")
    search_fields = ("user__username", "category__name")
