# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0007_element_caruse'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='element',
            name='caruse',
            field=models.OneToOneField(to='carusele.Listing'),
            preserve_default=True,
        ),
    ]
