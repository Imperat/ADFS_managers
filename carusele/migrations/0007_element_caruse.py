# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0006_auto_20150702_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='caruse',
            field=models.OneToOneField(default=None, to='carusele.Listing'),
            preserve_default=True,
        ),
    ]
