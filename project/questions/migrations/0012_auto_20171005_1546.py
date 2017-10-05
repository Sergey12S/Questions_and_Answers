# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0011_auto_20171005_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(verbose_name='ответ'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.PositiveIntegerField(default=0, verbose_name='рейтинг'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=255, verbose_name='заголовок'),
        ),
    ]
