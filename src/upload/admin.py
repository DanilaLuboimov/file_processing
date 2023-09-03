from django.contrib import admin

from .models import File


class FileAdmin(admin.ModelAdmin):
    readonly_fields = ("file", "upload_at", "processed",)
    list_display = ("id", "file", "upload_at", "processed",)


admin.site.register(File, FileAdmin)
