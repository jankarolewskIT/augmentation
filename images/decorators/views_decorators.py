import base64
import functools
import json
from io import BytesIO

from django.http import JsonResponse, HttpResponseBadRequest


def check_json(func):
    """
    Decorator for checking if request.body has valid keys
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        resp_json = json.dumps(request.body.decode('utf-8'))
        if not all(['img' in resp_json, 'format' in resp_json, 'img_name' in resp_json]):
            return JsonResponse({"error": "Request body does not contain required elements"})
        else:
            return func(request, *args, **kwargs)

    return wrapper


def decode(func):
    """
    Decorator for decoding data retrieved from request

    :param func: decorated function
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        kwargs["img"] = json.loads(request.body.decode("utf-8")).get("img")
        kwargs["format"] = json.loads(request.body.decode("utf-8")).get("format")
        kwargs["img_name"] = json.loads(request.body.decode("utf-8")).get("img_name")

        bytes_img = kwargs.get("img").encode("utf-8")

        original_data = base64.b64decode(bytes_img)
        kwargs["origin_buffer"] = BytesIO(original_data)

        return func(request, *args, **kwargs)

    return wrapper
