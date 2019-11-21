# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-11-19 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_webname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(null=True, verbose_name='用户头像路径'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(default='', help_text='不超过300字', max_length=300, verbose_name='个人简介'),
        ),
    ]