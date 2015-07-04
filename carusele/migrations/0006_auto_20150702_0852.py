# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carusele', '0005_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('content', models.TextField()),
                ('pubdate', models.DateTimeField()),
                ('image', models.ImageField(upload_to=b'media')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.AlterField(
            model_name='element',
            name='content',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
