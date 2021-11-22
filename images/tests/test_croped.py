import base64
import io
import json

from PIL import Image
from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase


class ImageCroppedViewTest(APITestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/augmentation/crop/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('cropped'))
        self.assertEqual(response.status_code, 200)

    def test_cropped_dimensions(self):
        """
        Iterates through json_file and makes requests.
        Check if cropped image size is lesser then initial image
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            initial_base64 = base64.b64decode(request.get("img"))
            initial_image = Image.open(io.BytesIO(initial_base64))

            initial_width, initial_height = initial_image.size

            left_param = 200
            top_param = 200
            right_param = 300
            bottom_param = 300

            response = self.client.post(
                path=f"/augmentation/crop/?left={left_param}&top={top_param}&right={right_param}&bottom={bottom_param}",
                data=json.dumps(request),
                content_type="application/json"

            )

            response_base64 = base64.b64decode(json.loads(response.content).get("base64_image"))
            response_cropped_image = Image.open(io.BytesIO(response_base64))

            cropped_width, cropped_height = response_cropped_image.size

            self.assertGreater(initial_width, cropped_width)
            self.assertGreater(initial_height, cropped_height)

    def test_response_400(self):
        """
        Check if request with invalid params returns response with status_code 400
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            left_param = 301
            top_param = 301
            right_param = 300
            bottom_param = 300

            response = self.client.post(
                path=f"/augmentation/crop/?left={left_param}&top={top_param}&right={right_param}&bottom={bottom_param}",
                data=json.dumps(request),
                content_type="application/json"

            )

            self.assertEqual(response.status_code, 400)
