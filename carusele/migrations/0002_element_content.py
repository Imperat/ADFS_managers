# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='content',
            field=models.TextField(null=2),
            preserve_default=True,
        ),
    ]
