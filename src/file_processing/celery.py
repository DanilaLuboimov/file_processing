import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_processing.settings")

app = Celery("file_processing")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
