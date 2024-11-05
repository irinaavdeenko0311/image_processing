from PIL import Image
from rest_framework import status
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Image
from .send import send_message
from .serializers import ImageCreateSerializer, ImageGetSerializer


class ImageListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageGetSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        file = request.FILES.get("image")
        serialized = ImageCreateSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.validated_data.pop("image")
        image = Image.objects.create(**serialized.validated_data)
        serialized = self.get_serializer(image)

        with file.open("rb") as f:
            binary_data = f.read()
        id = serialized.data.get("id")
        send_message(dict(src_file=binary_data, id=id))

        return Response(data=serialized.data, status=status.HTTP_201_CREATED)


class ImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageGetSerializer
