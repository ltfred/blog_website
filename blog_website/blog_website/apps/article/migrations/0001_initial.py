# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-11-07 22:07
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(help_text='b不超过50字', max_length=50, verbose_name='标题')),
                ('content', ckeditor.fields.RichTextField(verbose_name='内容')),
                ('read_count', models.IntegerField(default=0, verbose_name='阅读量')),
                ('index_image', models.CharField(max_length=1000, null=True, verbose_name='文章主图')),
                ('is_top', models.BooleanField(default=False, verbose_name='是否置顶')),
                ('like_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('describe', models.TextField(default='', help_text='用于列表页展示文章简介', verbose_name='文章描述')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(help_text='不超过20个字', max_length=20, verbose_name='名称')),
                ('describe', models.CharField(default='', help_text='不超过100个字', max_length=100, verbose_name='类别描述')),
                ('image_url', models.CharField(max_length=1000, null=True, verbose_name='类别图片')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='article.ArticleCategory', verbose_name='父类别')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': 'article_category',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(help_text='不超过20个字', max_length=20, verbose_name='文章标签')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'db_table': 'label',
            },
        ),
    ]
