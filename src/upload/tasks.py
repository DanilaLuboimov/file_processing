import json
import os
import logging

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

from utils.exceptions import CorrectExtFile, RawFileFormat
from .models import File

logger = logging.getLogger(__name__)


@shared_task
def process_file(file_id: int):
    """Определение расширения файла и последующая обработкой,
    если такая возможна, в фоновом режиме"""
    file: File = File.objects.get(id=file_id)
    old_file_path: str = file.file.path
    file_ext: str = old_file_path.split(".")[-1]

    try:
        if file_ext in ("json", "jpeg",):
            raise CorrectExtFile
        elif file_ext in ("bmp", "tif", "psd", "gif", "png", "jpg",):
            change_image_file(file)
        elif file_ext == "txt":
            change_text_file(file)
        else:
            raise RawFileFormat
    except CorrectExtFile:
        pass
    except RawFileFormat:
        logger.warning(f"File ID [{file.id}] Необработанный "
                       f"файл формата .{file_ext}")
    except Exception as e:
        logger.error(f"File ID [{file.id}] {e}")
        return False
    else:
        os.remove(os.path.abspath(os.path.join(
            settings.BASE_DIR, old_file_path
        )))

    file.processed = True
    file.save()
    return True


def resize_image(file: str, size: tuple[int]) -> BytesIO:
    """Обработка изображений"""
    image: Image = Image.open(file)

    if image.mode in ("RGBA", "P"):
        image: Image = image.convert("RGB")

    image: Image = image.resize(size)
    buffer: BytesIO = BytesIO()
    image.save(buffer, format="JPEG")
    return buffer.getvalue()


def change_image_file(file: File) -> None:
    """Сохранение обработанного изображения"""
    new_img: BytesIO = resize_image(file.file, (1280, 720))
    file.file.save(f"{file.id}.jpeg", ContentFile(new_img), save=True)


def change_text_file(file: File) -> None:
    """Проверяет возможность декодировать txt-формат файлов
    и преобразует в json. В ином случае ничего не меняет"""
    try:
        with open(file.file.path, "r", encoding="utf-8") as _:
            data: list[dict] = json.load(_)
            new_file: str = os.path.join(
                settings.MEDIA_ROOT, "files/new_file.json"
            )
            with open(new_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        with open(new_file, "r", encoding="utf-8") as f:
            file.file.save(f"{file.id}.json", f, save=True)

        os.remove(new_file)
    except json.JSONDecodeError:
        logger.warning(f"File ID [{file.id}] имеет формат .txt, но "
                       f"не может декодироваться в json")
        raise CorrectExtFile
