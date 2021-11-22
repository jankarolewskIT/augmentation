import base64
from io import BytesIO

from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from .decorators.views_decorators import decode, check_json
from .models import MediaImage
from .serializers import MediaImageSerializer
from .utils import encode_img


@check_json
@decode
def img_resize_view(request, *args, **kwargs):
    """
    Converts an base64 decoded image (type:str) to Pillow.Image object.
    Creates a new image on base of the one retrieved from request.
    Resizes a new image accordingly to parameters from request.
    Encodes new image to base64 str, saves this image as MediaImage object in DB.
    :param request:
    :return: JsonResponse
    """
    width = request.GET.get("width")
    height = request.GET.get("height")

    pillow_img = Image.open(kwargs.get('origin_buffer'))
    new_image = pillow_img.resize((int(width), int(height)))

    buffer = BytesIO()

    encoded_info = encode_img(new_image, buffer, kwargs.get('format'))

    obj = MediaImage.objects.create(
        image_path=ContentFile(encoded_info[0], f'resized_{kwargs.get("img_name")}.jpg'),
        base64_image=encoded_info[1],
        img_name=f'resized_{kwargs.get("img_name")}_w{width}_h{height}',
        format=kwargs.get('format').upper()
    )

    serializer = MediaImageSerializer(obj)

    return JsonResponse(data=serializer.data)


@check_json
@decode
def img_crop_view(request, *args, **kwargs):
    """
    Converts an base64 decoded image (type:str) to Pillow.Image object.
    Creates a new image on base of the one retrieved from request.
    Crops an image accordingly to parameters from request.
    Encodes new image to base64 str, saves this image as MediaImage object in DB.
    :param request:
    :return: JsonResponse
    """

    left = int(request.GET.get('left'))
    top = int(request.GET.get('top'))
    right = int(request.GET.get('right'))
    bottom = int(request.GET.get('bottom'))

    crop_box = (
        left, top, right, bottom
    )

    if left > right or top > bottom:
        return HttpResponseBadRequest(
            "Provided parameters are not valid. Left can not be greater than right, and top can not be greater than bottom")

    pillow_img = Image.open(kwargs.get('origin_buffer'))
    buffer = BytesIO()

    new_image = pillow_img.crop(crop_box)

    encoded_info = encode_img(new_image, buffer, kwargs.get('format'))

    obj = MediaImage.objects.create(
        image_path=ContentFile(encoded_info[0], f'cropped_{kwargs.get("img_name")}.jpg'),
        base64_image=encoded_info[1],
        format=kwargs.get('format').upper(),
        img_name=f'cropped_{kwargs.get("img_name")}'
    )

    serializer = MediaImageSerializer(obj)
    return JsonResponse(data=serializer.data)


@check_json
@decode
def img_rotate_view(request, *args, **kwargs):
    """
    Converts an base64 decoded image (type:str) to Pillow.Image object.
    Creates a new image on base of the one retrieved from request.
    Rotate an image accordingly to parameters from request.
    Encodes new image to base64 str, saves this image as MediaImage object in DB.
    :param request:
    :return: JsonResponse
    """
    angle = int(request.GET.get('angle'))

    pillow_img = Image.open(kwargs.get('origin_buffer'))
    buffer = BytesIO()

    new_image = pillow_img.rotate(angle)

    encoded_info = encode_img(new_image, buffer, kwargs.get('format'))

    obj = MediaImage.objects.create(
        image_path=ContentFile(encoded_info[0], f'rotated_{kwargs.get("img_name")}.jpg'),
        base64_image=encoded_info[1],
        format=kwargs.get('format').upper(),
        img_name=f'rotated_{kwargs.get("img_name")}_r{angle}'
    )

    serializer = MediaImageSerializer(obj)

    return JsonResponse(data=serializer.data)


@check_json
@decode
def img_negative_view(request, *args, **kwargs):
    """
    Converts an base64 decoded image (type:str) to Pillow.Image object.
    Creates a new image on base of the one retrieved from request.
    Function changes an image to it's negative version.
    Encodes new image to base64 str, saves this image as MediaImage object in DB.
    :param request:
    :return: JsonResponse
    """

    pillow_img = Image.open(kwargs.get("origin_buffer")).convert("RGB")

    buffer = BytesIO()
    new_image = ImageOps.invert(pillow_img)

    encoded_info = encode_img(new_image, buffer, kwargs.get('format'))

    edited_img = MediaImage.objects.create(
        image_path=ContentFile(encoded_info[0], f'negative_{kwargs.get("img_name")}.{kwargs.get("format").lower()}'),
        base64_image=encoded_info[1],
        format=kwargs.get('format').upper(),
        img_name=f'negative_{kwargs.get("img_name")}'

    )

    obj = get_object_or_404(MediaImage, id=edited_img.id)
    serializer = MediaImageSerializer(obj)
    return JsonResponse(data=serializer.data)


@check_json
@decode
def img_compression_view(request, *args, **kwargs):
    """
    Converts an base64 decoded image (type:str) to Pillow.Image object.
    Creates a new image on base of the one retrieved from request.
    Compress a new image accordingly to parameters from request.
    q < 100 -> lossy compression

    Encodes new image to base64 str, saves this image as MediaImage object in DB.
    :param request:
    :return: JsonResponse
    """
    quality = int(request.GET.get('q'))

    new_image = Image.open(kwargs.get("origin_buffer"))

    buffer = BytesIO()

    new_image.save(buffer, format=kwargs.get('format'), optimize=True, quality=quality)

    new_image_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    new_image_data = base64.b64decode(new_image_str)

    obj = MediaImage.objects.create(
        image_path=ContentFile(new_image_data, f'compressed_{kwargs.get("img_name")}.jpg'),
        base64_image=new_image_str,
        format=kwargs.get('format').upper(),
        img_name=f'compressed_{kwargs.get("img_name")}'

    )

    serializer = MediaImageSerializer(obj)

    return JsonResponse(data=serializer.data)
