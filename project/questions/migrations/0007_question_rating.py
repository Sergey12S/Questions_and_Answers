# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-02 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_remove_question_f'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
