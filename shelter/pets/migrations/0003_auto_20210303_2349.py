# Generated by Django 3.1.5 on 2021-03-03 20:49

import django.core.validators
from django.db import migrations, models
import pets.models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_auto_20210301_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(blank=True, upload_to=pets.models.path_for_pet_img, validators=[django.core.validators.validate_image_file_extension], verbose_name='Фото'),
        ),
    ]
