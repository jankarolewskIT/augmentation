import json

from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase


class ImageCompressionViewTest(APITestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/augmentation/compression/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('compressed'))
        self.assertEqual(response.status_code, 200)

    def test_compression(self):
        """
        Makes a lossy compression image and
        then checks if another compression with q=100 does not change an image
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            quality = 10
            response_compressed = self.client.post(
                path=f'/augmentation/compression/?q={quality}',
                data=json.dumps(request),
                content_type='application/json'
            )

            compressed_base64 = json.loads(response_compressed.content).get("base64_image")

            pload = {
                "img": compressed_base64,
                "format": json.loads(response_compressed.content).get("format"),
                "img_name": json.loads(response_compressed.content).get("img_name"),
            }

            same_quality = 100
            shuffle_uncompressed_response = self.client.post(
                path=f'/augmentation/compression/?q={same_quality}',
                data=json.dumps(pload),
                content_type='application/json'
            )

            shuffle_base64 = json.loads(shuffle_uncompressed_response.content).get("base64_image")

            self.assertEqual(compressed_base64, shuffle_base64)
