# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0004_sparkterasortinformation_smt'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparkterasortinformation',
            name='cores',
            field=models.PositiveIntegerField(default=8, verbose_name='Number of cores'),
        ),
        migrations.AddField(
            model_name='sparkterasortinformation',
            name='executor_memory',
            field=models.PositiveIntegerField(default=4, verbose_name='Executor-memory(GB)'),
        ),
    ]
