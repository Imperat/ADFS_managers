# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0002_element_content'),
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
        migrations.AddField(
            model_name='element',
            name='news',
            field=models.OneToOneField(default=None, to='carusele.News'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='element',
            name='image',
            field=models.ImageField(upload_to=b'media'),
            preserve_default=True,
        ),
    ]
