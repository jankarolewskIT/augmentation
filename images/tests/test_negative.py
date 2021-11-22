import json

from django.conf import settings
from django.shortcuts import reverse
from rest_framework.test import APITestCase


class ImageNegativeViewTest(APITestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/augmentation/negative/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('negative'))
        self.assertEqual(response.status_code, 200)

    def test_negative(self):
        """
        Double negates an image and check if base64 string is the same.
        """
        with open(f"{settings.BASE_DIR}/json_data.json", "r") as json_file:
            data = json.load(json_file)
        for request in data:
            response_negative = self.client.post(
                path='/augmentation/negative/',
                data=json.dumps(request),
                content_type='application/json'
            )

            conversion_pload = {
                "img": json.loads(response_negative.content).get('base64_image').replace("\'", "\""),
                "format": json.loads(response_negative.content).get('format').replace("\'", "\""),
                "img_name": json.loads(response_negative.content).get('img_name').replace("\'", "\"")
            }

            shuffle_response = self.client.post(
                path='/augmentation/negative/',
                data=json.dumps(conversion_pload),
                content_type='application/json'
            )

            shuffled_plod = {
                "img": json.loads(shuffle_response.content).get('base64_image').replace("\'", "\""),
                "format": json.loads(shuffle_response.content).get('format').replace("\'", "\""),
                "img_name": json.loads(shuffle_response.content).get('img_name').replace("\'", "\"")
            }

            restored_negative_response = self.client.post(
                path='/augmentation/negative/',
                data=json.dumps(shuffled_plod),
                content_type='application/json'
            )

            converted_negative_base64 = json.loads(response_negative.content).get("base64_image")
            converted_negative_format = json.loads(response_negative.content).get("format")
            shuffled_negative_base64 = json.loads(restored_negative_response.content).get("base64_image")
            shuffled_negative_format = json.loads(restored_negative_response.content).get("format")

            self.assertEqual(converted_negative_base64, shuffled_negative_base64)
            self.assertEqual(converted_negative_format, shuffled_negative_format)
