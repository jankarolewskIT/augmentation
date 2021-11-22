from django.contrib import admin

from .models import MediaImage

admin.site.register(MediaImage, admin.ModelAdmin)
