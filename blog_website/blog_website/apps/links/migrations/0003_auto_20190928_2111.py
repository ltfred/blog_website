# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-09-28 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0002_auto_20190927_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='link',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]