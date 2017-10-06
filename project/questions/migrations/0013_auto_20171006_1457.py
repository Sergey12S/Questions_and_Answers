# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-06 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_auto_20171005_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.AddField(
            model_name='question',
            name='categories',
            field=models.ManyToManyField(related_name='questions', to='questions.Category'),
        ),
    ]
