import logging

from rest_framework import generics
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import process_file
from .models import File
from .serializers import FileUploadSerializer, FileAllSerializer

logger = logging.getLogger(__name__)


class FileCreateNew(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Принимает post-запросы по api/upload/ form-data
        для загрузки файлов на сервер"""
        serializer: FileUploadSerializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            file: File = serializer.save()
            process_file.delay(file.id)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        logger.warning(f"{serializer.errors}")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FileAll(generics.ListAPIView):
    serializer_class = FileAllSerializer
    queryset = File.objects.all()
