# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repair', '0011_auto_20171118_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enquiry',
            old_name='condition',
            new_name='deviceCondition',
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='status',
            field=models.CharField(choices=[('EN', 'Enquired'), ('CH', 'Checked'), ('RE', 'Repaired'), ('DO', 'Done'), ('RJ', 'Rejected')], default='EN', max_length=3),
        ),
    ]
