from django.urls import path

from .views import img_negative_view, img_resize_view, img_crop_view, img_rotate_view, img_compression_view

urlpatterns = [
    path('resize/', img_resize_view, name='resize'),
    path("crop/", img_crop_view, name='cropped'),
    path("rotate/", img_rotate_view, name='rotated'),
    path("compression/", img_compression_view, name='compressed'),
    path("negative/", img_negative_view, name='negative'),
]
