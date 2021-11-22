import json

from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase


class ImageRotateViewTest(APITestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/augmentation/rotate/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('rotated'))
        self.assertEqual(response.status_code, 200)

    def test_rotation(self):
        """
        Rotate an image and check if another full rotation return the same base64_image
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            initial_request_format = request.get('format')
            angle = 90
            rotated_response = self.client.post(f'/augmentation/rotate/?angle={angle}', json.dumps(request),
                                                content_type='application/json')

            full_rotation = 360

            rotation_pload = {
                "img": json.loads(rotated_response.content).get("base64_image").replace("\'", "\""),
                "format": json.loads(rotated_response.content).get("format").replace("\'", "\""),
                "img_name": json.loads(rotated_response.content).get("img_name").replace("\'", "\""),

            }

            full_rotation_response = self.client.post(
                f'/augmentation/rotate/?angle={full_rotation}',
                json.dumps(rotation_pload),
                content_type='application/json'
            )

            initial_rotation_base64 = json.loads(rotated_response.content).get('base64_image')

            restored_rotated_base64 = json.loads(full_rotation_response.content).get('base64_image')
            restore_rotated_format = json.loads(full_rotation_response.content).get('format')

            self.assertGreater(initial_rotation_base64, restored_rotated_base64)
            self.assertEqual(initial_request_format, restore_rotated_format)
