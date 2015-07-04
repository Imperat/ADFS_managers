# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamlogic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualExperience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beginDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecOfTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experience', models.OneToOneField(to='teamlogic.ActualExperience')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('foundation', models.IntegerField()),
                ('image', models.ImageField(upload_to=b'media')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recofteam',
            name='team',
            field=models.ManyToManyField(to='teamlogic.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='history',
            field=models.ManyToManyField(to='teamlogic.RecOfTeam'),
            preserve_default=True,
        ),
    ]
