# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lolpath', '0009_remove_matchreg_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchreg',
            name='duration',
            field=models.IntegerField(verbose_name='Duration'),
        ),
    ]
