import base64
import io
import json

from PIL import Image
from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase


class ImageResizeViewTest(APITestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/augmentation/resize/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('resize'))
        self.assertEqual(response.status_code, 200)

    def test_resized_dimension(self):
        """
        Compare dimensions of initial image and new_image
        Check if given params are greater/smaller then initial width and height of an image.
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            initial_base64 = base64.b64decode(request.get("img"))
            initial_image = Image.open(io.BytesIO(initial_base64))

            initial_width, initial_height = initial_image.size

            width_param = 200
            height_param = 200

            resized_response = self.client.post(
                path=f"/augmentation/resize/?width={width_param}&height={height_param}",
                data=json.dumps(request),
                content_type="application/json"
            )

            resized_image_base64 = base64.b64decode(json.loads(resized_response.content).get("base64_image"))

            resized_image = Image.open(io.BytesIO(resized_image_base64))

            resized_width, resized_height = resized_image.size

            if initial_width > width_param:
                self.assertGreater(initial_width, resized_width)
            elif initial_width == width_param:
                self.assertEqual(initial_width, resized_width)
            else:
                self.assertGreater(resized_width, initial_width)

            if initial_height > height_param:
                self.assertGreater(initial_height, resized_height)
            elif initial_height == height_param:
                self.assertEqual(initial_height, resized_height)
            else:
                self.assertGreater(resized_height, initial_height)
