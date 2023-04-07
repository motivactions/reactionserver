from django.contrib import admin

from .models import Bookmark, Flag, Reaction, Review


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["user", "application", "object_type", "object_id"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "application", "object_type", "object_id"]


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ["user", "application", "object_type", "object_id"]
    list_filter = ["value"]


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ["user", "application", "object_type", "object_id", "value"]
    list_filter = ["value"]
