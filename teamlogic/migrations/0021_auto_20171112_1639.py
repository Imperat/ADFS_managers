# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-11-12 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamlogic', '0020_auto_20170722_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeboard',
            name='match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamlogic.Match'),
        ),
    ]
