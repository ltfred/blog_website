# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-13 17:34
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_auto_20200313_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=ckeditor.fields.RichTextField(verbose_name='内容'),
        ),
    ]