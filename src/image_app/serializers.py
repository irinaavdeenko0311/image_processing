from rest_framework import serializers

from .models import Image


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Image
        fields = ["name", "description", "image"]


class ImageGetSerializer(serializers.ModelSerializer):
    src_url = serializers.URLField(read_only=True)
    dst_url = serializers.URLField(read_only=True)
    resolution = serializers.CharField(read_only=True)
    size = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Image
        fields = "__all__"

    def to_representation(self, instance: Image) -> dict:
        representation = super().to_representation(instance)
        result = {}
        for k, v in representation.items():
            if v is not None:
                result[k] = v
        return result
