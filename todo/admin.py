from django.contrib import admin
from .models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_complete", "created_at", "updated_at")
    list_filter = ("is_complete", "created_at")
    search_fields = ("title",)
