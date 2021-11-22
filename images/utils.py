import base64


def encode_img(image, buffer, format_):
    """
    Function ensure that Image object has mode == RGB or L
    Then encode this image to base64

    :param image: PIL.Image object
    :param buffer: Binary object
    :param format_: str
    :return: tuple(base64_binary, base64_str)
    """
    if image.mode not in ('RGB', 'L'):
        image.convert('RGB').save(buffer, format=format_)
    else:
        image.save(buffer, format=format_)

    new_image_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    new_image_data = base64.b64decode(new_image_str)

    return new_image_data, new_image_str
