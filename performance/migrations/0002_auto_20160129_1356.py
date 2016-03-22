# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='speccpumachine',
            name='existing_l4_speccpu',
            field=models.BooleanField(verbose_name='Open L4 Cache', default=True),
        ),
        migrations.AddField(
            model_name='speccpumachine',
            name='half_l3_speccpu',
            field=models.BooleanField(verbose_name='Half L3 Cache', default=False),
        ),
    ]
