# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20171001_1029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created_at',), 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
    ]
