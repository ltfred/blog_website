# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-11-19 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_auto_20191119_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.CharField(help_text='必须以http/https开头', max_length=1000, verbose_name='链接'),
        ),
    ]
