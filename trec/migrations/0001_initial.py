# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_pic', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('website', models.URLField(blank=True)),
                ('display_name', models.CharField(max_length=128)),
                ('organisation', models.CharField(max_length=128, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('results_file', models.FileField(upload_to=b'')),
                ('map', models.FloatField()),
                ('p10', models.FloatField()),
                ('p20', models.FloatField()),
                ('runType', models.CharField(max_length=1, choices=[(b'a', b'Automatic'), (b'm', b'Manual')])),
                ('queryType', models.CharField(max_length=6, choices=[(b'title', b'Title'), (b'ti+des', b'Title and description'), (b'dscrp', b'Description'), (b'all', b'All'), (b'other', b'Other')])),
                ('feedbackType', models.CharField(max_length=5, choices=[(b'none', b'None'), (b'pseud', b'Pseudo'), (b'rel', b'Relevance'), (b'other', b'Other')])),
                ('researcher', models.ForeignKey(to='trec.Researcher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=128)),
                ('task_url', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('year', models.TimeField()),
                ('judgementFile', models.FileField(upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=128)),
                ('track_url', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('genre', models.CharField(max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='track',
            field=models.ForeignKey(to='trec.Track'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='run',
            name='task',
            field=models.ForeignKey(to='trec.Task'),
            preserve_default=True,
        ),
    ]
