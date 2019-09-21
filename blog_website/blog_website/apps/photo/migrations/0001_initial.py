# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-09-21 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=10, verbose_name='照片标题')),
                ('url', models.CharField(max_length=200, verbose_name='照片地址')),
            ],
            options={
                'verbose_name': '照片',
                'verbose_name_plural': '照片',
                'db_table': 'photos',
            },
        ),
        migrations.CreateModel(
            name='PhotoCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=10, verbose_name='相册类名')),
            ],
            options={
                'verbose_name': '相册类别',
                'verbose_name_plural': '相册类别',
                'db_table': 'photo_category',
            },
        ),
        migrations.AddField(
            model_name='photo',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='photos', to='photo.PhotoCategory', verbose_name='照片类别'),
        ),
    ]