# Generated by Django 3.2.9 on 2021-11-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_auto_20211118_1931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediaimage',
            old_name='image',
            new_name='image_path',
        ),
        migrations.AddField(
            model_name='mediaimage',
            name='format',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='mediaimage',
            name='img_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
