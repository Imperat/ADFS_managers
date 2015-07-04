# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0003_auto_20150630_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='news',
        ),
        migrations.DeleteModel(
            name='News',
        ),
    ]
