# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-10-07 13:56
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20201007_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Uddhav\\Desktop\\Django-Ecommerce\\static_cdn\\protected_media'), upload_to=products.models.upload_product_file_loc),
        ),
    ]
