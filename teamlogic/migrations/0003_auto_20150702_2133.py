# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('teamlogic', '0002_auto_20150702_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recofteam',
            name='experience',
        ),
        migrations.DeleteModel(
            name='ActualExperience',
        ),
        migrations.AddField(
            model_name='recofteam',
            name='beginDate',
            field=models.DateField(default=datetime.datetime(2015, 7, 2, 21, 33, 16, 460483)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recofteam',
            name='endDate',
            field=models.DateField(default=datetime.datetime(2015, 7, 2, 21, 33, 16, 460545)),
            preserve_default=True,
        ),
    ]
