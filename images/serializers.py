from rest_framework import serializers
# from images.loaders.request_data_loader import create_request_data
import images.loaders.test_image_loader
from .models import MediaImage


class MediaImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MediaImage
        fields = ['id', 'image_path', 'base64_image', 'format', 'img_name']
