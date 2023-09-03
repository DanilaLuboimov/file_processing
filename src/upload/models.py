from django.db import models

from utils.models import path_and_rename


class File(models.Model):
    file = models.FileField(
        upload_to=path_and_rename("files/"),
        verbose_name="Файл"
    )
    upload_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
    )
    processed = models.BooleanField(
        default=False,
        verbose_name="Обработка",
    )

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        db_table = "files"

