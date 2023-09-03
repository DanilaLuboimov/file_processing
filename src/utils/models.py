import os


from django.utils.deconstruct import deconstructible
from uuid import uuid4


def path_and_rename(path):
    return PathRename(path)


@deconstructible
class PathRename:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{ext}"
        return os.path.join(f"{self.path}", filename)
