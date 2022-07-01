from django.contrib import admin

# Register your models here.
from app_manager.models import LstStatus


@admin.register(LstStatus)
class LstStatusAdmin(admin.ModelAdmin):
    list_display = (
        "status",
        "word",
    )
    list_editable = (
        "word",
    )
