# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=70)),
                ('lastName', models.CharField(max_length=70)),
                ('birth', models.DateField()),
                ('vkLink', models.CharField(max_length=30)),
                ('basePosition', models.CharField(max_length=1)),
                ('image', models.ImageField(upload_to=b'media')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
