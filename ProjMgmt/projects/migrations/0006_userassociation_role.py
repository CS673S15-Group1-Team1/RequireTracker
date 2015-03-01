# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20150228_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassociation',
            name='role',
            field=models.CharField(default='user', max_length=128),
            preserve_default=False,
        ),
    ]
