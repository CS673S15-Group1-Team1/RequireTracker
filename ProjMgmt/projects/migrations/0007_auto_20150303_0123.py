# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_userassociation_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={},
        ),
        migrations.RemoveField(
            model_name='userassociation',
            name='role',
        ),
    ]
