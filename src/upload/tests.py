import json
import os
import tempfile

from django.conf import settings
from django.urls import reverse
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image

from .models import File
from.tasks import process_file


class FileTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """Создание тестовых данных"""
        files_dir = os.path.join(settings.BASE_DIR, "media/files/")

        with open(f"{files_dir}text.txt", "w") as f:
            f.write("grtw45hijlu")

        file_1: File = File.objects.create(file=f"{files_dir}text.txt")
        file_1.save()

        with open(f"{files_dir}make_to_json.txt", "w") as f:
            data: list[dict] = [{"foo": "bar"}]
            json.dump(data, f, indent=4, ensure_ascii=False)

        file_2: File = File.objects.create(file=f"{files_dir}make_to_json.txt")
        file_2.save()

        with open(f"{files_dir}json.json", "w") as f:
            data: list[dict] = [{"foo": "bar"}]
            json.dump(data, f, indent=4, ensure_ascii=False)

        file_3: File = File.objects.create(file=f"{files_dir}json.json")
        file_3.save()

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND="memory")
    def test_post_file(self):
        """Тестирование правильной работы endpoint 'upload/'"""
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        res = self.client.post(
            reverse("upload-file", ), data={"file": tmp_file},
            format="multipart"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        files: File = File.objects.all()
        self.assertEqual(len(files), 4)

    def test_bad_post_file(self):
        """Тестирование работы endpoint 'upload/' при некорректных данных"""
        res = self.client.post(
            reverse("upload-file", ), data={"file": "asdfghjkl;"},
            format="multipart"
        )
        files: File = File.objects.all()
        self.assertEqual(len(files), 3)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rename_file(self):
        """Тестирование обработки файла"""
        file: File = File.objects.get(id=2)
        old_path: str = file.file.path
        process_file(2)
        file: File = File.objects.get(id=2)
        new_path: str = file.file.path
        self.assertFalse(old_path == new_path)
        self.assertEqual(file.processed, True)

    def test_txt_to_txt(self):
        """Тестирование обработки txt формата, при
        невозможности декодироваться в json"""
        file: File = File.objects.get(id=1)
        old_path: str = file.file.path
        process_file(1)
        file: File = File.objects.get(id=1)
        new_path: str = file.file.path
        self.assertTrue(old_path == new_path)
        self.assertEqual(file.processed, True)

    def test_correct_ext_file(self):
        """Тестирование формата json, как файла, который
        не подлежит обработке"""
        file: File = File.objects.get(id=3)
        old_path: str = file.file.path
        process_file(3)
        file: File = File.objects.get(id=3)
        new_path: str = file.file.path
        self.assertTrue(old_path == new_path)
        self.assertEqual(file.processed, True)

    def test_correct_response_files(self):
        """Тестирование endpoint 'files/'"""
        res = self.client.get(reverse("file-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 3)
