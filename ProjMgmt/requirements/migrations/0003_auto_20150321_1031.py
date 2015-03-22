# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requirements', '0002_auto_20150321_0539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(default=b'', max_length=1024, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='iterations',
            field=models.ManyToManyField(to='requirements.Iteration'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='story',
            name='iteration',
            field=models.ForeignKey(blank=True, to='requirements.Iteration', null=True),
            preserve_default=True,
        ),
    ]
