# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=2)),
                ('min', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_goal', models.IntegerField()),
                ('away_goal', models.IntegerField()),
                ('home_goal_first', models.IntegerField()),
                ('away_goal_first', models.IntegerField()),
                ('technical', models.BooleanField(default=None)),
                ('date_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MatchInLeague',
            fields=[
                ('match_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='teamlogic.Match')),
                ('tour', models.IntegerField(default=2)),
                ('hasResult', models.BooleanField(default=False)),
                ('register', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('teamlogic.match',),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstName', models.CharField(max_length=70)),
                ('lastName', models.CharField(max_length=70)),
                ('birth', models.DateField()),
                ('vkLink', models.CharField(max_length=30, null=True)),
                ('basePosition', models.CharField(max_length=1)),
                ('image', models.ImageField(upload_to=b'media')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecOfTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beginDate', models.DateField(default=datetime.datetime(2015, 7, 11, 19, 9, 31, 248158))),
                ('endDate', models.DateField(default=datetime.datetime(2015, 7, 11, 19, 9, 31, 248209))),
                ('number', models.IntegerField(default=-1)),
                ('player', models.ForeignKey(to='teamlogic.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('accr', models.BooleanField(default=True)),
                ('description', models.TextField(default=b'olo')),
                ('estimate', models.FloatField()),
                ('physics', models.IntegerField()),
                ('image', models.ImageField(default=b'/media/404/', upload_to=b'media')),
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
                ('vkLink', models.CharField(default=b'nulls', max_length=30, null=True)),
                ('captain', models.OneToOneField(related_name='+', to='teamlogic.Player')),
                ('home', models.ForeignKey(to='teamlogic.Stadium')),
                ('players', models.ManyToManyField(to='teamlogic.Player', through='teamlogic.RecOfTeam')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamInLeague',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goal_s', models.IntegerField()),
                ('goal_p', models.IntegerField()),
                ('match_v', models.IntegerField()),
                ('match_n', models.IntegerField()),
                ('match_p', models.IntegerField()),
                ('straf', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('image', models.ImageField(upload_to=b'')),
                ('matchs', models.ManyToManyField(to='teamlogic.MatchInLeague')),
                ('members', models.ManyToManyField(to='teamlogic.Team', through='teamlogic.TeamInLeague')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='teaminleague',
            name='league',
            field=models.ForeignKey(to='teamlogic.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teaminleague',
            name='team',
            field=models.ForeignKey(to='teamlogic.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stadium',
            name='home',
            field=models.ManyToManyField(to='teamlogic.Team', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recofteam',
            name='team',
            field=models.ForeignKey(to='teamlogic.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='history',
            field=models.ManyToManyField(to='teamlogic.Team', null=True, through='teamlogic.RecOfTeam'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='away',
            field=models.ForeignKey(related_name='+', to='teamlogic.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='away_goals',
            field=models.ManyToManyField(related_name='away', to='teamlogic.Goal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home',
            field=models.ForeignKey(related_name='+', to='teamlogic.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home_goals',
            field=models.ManyToManyField(related_name='home', to='teamlogic.Goal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='league',
            field=models.ForeignKey(default=1, to='teamlogic.Tournament', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='place',
            field=models.ForeignKey(to='teamlogic.Stadium'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='autor',
            field=models.ForeignKey(to='teamlogic.Player'),
            preserve_default=True,
        ),
    ]
