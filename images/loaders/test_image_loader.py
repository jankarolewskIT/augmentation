import random
import string

import requests

from django.conf import settings

"""
Module runs get_test_image function 50 times for test purposes 
"""

def get_test_image(url: str) -> None:
    """
    Loads random images to BASE_DIR/test_images directory
    :param url:
    :return: None
    """
    formats = ["jpeg", "png", "bmp"]
    size = 10
    response = requests.get(url)
    file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))
    with open(f"{settings.BASE_DIR}/test_images/{file_name}.{random.choice(formats)}", "wb") as file:
        file.write(response.content)


if __name__ == '__main__':
    for _ in range(50):
        URL = f"https://picsum.photos/{random.randint(50, 500)}/{random.randint(50, 500)}"
        get_test_image(URL)
