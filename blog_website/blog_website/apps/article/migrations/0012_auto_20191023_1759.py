# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-23 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0011_auto_20191001_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(help_text='不超过20个字', max_length=20, verbose_name='文章标签'),
        ),
    ]