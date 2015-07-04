# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teamlogic', '0004_auto_20150704_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recofteam',
            name='beginDate',
            field=models.DateField(default=datetime.datetime(2015, 7, 4, 11, 46, 57, 99028)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recofteam',
            name='endDate',
            field=models.DateField(default=datetime.datetime(2015, 7, 4, 11, 46, 57, 99073)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recofteam',
            name='player',
            field=models.ForeignKey(default=None, to='teamlogic.Player'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='players',
            field=models.ManyToManyField(to='teamlogic.Player', through='teamlogic.RecOfTeam'),
            preserve_default=True,
        ),
    ]
