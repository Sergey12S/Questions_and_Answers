# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_auto_20171005_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Category'),
        ),
    ]
