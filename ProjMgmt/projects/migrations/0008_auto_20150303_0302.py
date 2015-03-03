# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20150303_0123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('own_project', 'Can own and create projects'),)},
        ),
        migrations.AddField(
            model_name='userassociation',
            name='role',
            field=models.CharField(default='user', max_length=128),
            preserve_default=False,
        ),
    ]
