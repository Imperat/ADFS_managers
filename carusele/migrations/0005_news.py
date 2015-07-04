# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0004_auto_20150630_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(default=b'None')),
                ('content', models.TextField()),
                ('likes', models.IntegerField()),
                ('tags', models.TextField()),
                ('pubDate', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
