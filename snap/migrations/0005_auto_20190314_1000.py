# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-14 10:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snap', '0004_auto_20190313_1929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='image',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
