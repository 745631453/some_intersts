# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 02:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ind', '0003_usermodel_u_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='MineModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_ticket', models.CharField(max_length=225)),
                ('m_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'axf_user_tic',
            },
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='u_ticket',
        ),
        migrations.AddField(
            model_name='minemodel',
            name='m',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Ind.MinModel'),
        ),
    ]