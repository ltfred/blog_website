# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-07 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=10, verbose_name='留言人')),
                ('email', models.CharField(max_length=50, verbose_name='邮箱')),
                ('content', models.TextField(verbose_name='留言内容')),
            ],
            options={
                'verbose_name': '留言',
                'verbose_name_plural': '留言',
                'db_table': 'message',
            },
        ),
    ]