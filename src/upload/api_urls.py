from django.urls import path
from .api_views import FileCreateNew, FileAll

urlpatterns = [
    path('upload/', FileCreateNew.as_view(), name='upload-file'),
    path('files/', FileAll.as_view(), name='file-list'),
]