import base64
import json
import os

from django.conf import settings


def create_request_data() -> None:
    """
    Function called at the beginning of container is run, to populate json_data file.
    :return: None
    """
    directory = os.fsencode(f"{settings.BASE_DIR}/test_images/")
    request_list = []
    for image in os.listdir(directory):
        image = image.decode('utf-8')
        with open(f"{settings.BASE_DIR}/test_images/{image}", "rb") as file:
            img_name, format_ = image.split('.')
            base64_str = base64.b64encode(file.read()).decode('utf-8')

            request = {
                "img": base64_str,
                "img_name": img_name,
                "format": format_.upper()
            }

            request_list.append(request)
        with open(f"{settings.BASE_DIR}/json_data.json", "w") as file:
            json.dump(request_list, file, indent=4)


if __name__ == "__main__":
    create_request_data()
