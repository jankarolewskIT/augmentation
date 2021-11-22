from django.db import models


class MediaImage(models.Model):
    """
    Image model for illustration purposes
    """
    image_path = models.ImageField(upload_to='img')
    base64_image = models.TextField(null=True)
    format = models.CharField(max_length=10, null=True)
    img_name = models.CharField(max_length=200, null=True)
