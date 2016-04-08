# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0003_sparkterasortinformation_bench_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparkterasortinformation',
            name='smt',
            field=models.PositiveIntegerField(default=4, verbose_name='SMT'),
        ),
    ]
