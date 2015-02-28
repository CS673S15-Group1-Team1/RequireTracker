# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20150217_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': (('own_project', 'Can own and create projects'),)},
        ),
    ]
