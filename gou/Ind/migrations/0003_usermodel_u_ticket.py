# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ind', '0002_auto_20180507_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='u_ticket',
            field=models.CharField(max_length=30, null=True),
        ),
    ]