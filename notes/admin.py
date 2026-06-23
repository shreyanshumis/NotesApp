from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "updated_at", "created_at")
    list_filter = ("owner", "created_at", "updated_at")
    search_fields = ("title", "content", "owner__username", "owner__email")
    ordering = ("-updated_at",)
