# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-08-04 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=39.99, max_digits=10),
        ),
    ]
