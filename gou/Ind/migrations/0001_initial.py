# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainDao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'index_dao',
            },
        ),
        migrations.CreateModel(
            name='MainLun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'index_lun',
            },
        ),
        migrations.CreateModel(
            name='MainMustBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'index_mustby',
            },
        ),
        migrations.CreateModel(
            name='MainShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
                ('categoryid', models.CharField(max_length=16)),
                ('brandname', models.CharField(max_length=100)),
                ('img1', models.CharField(max_length=200)),
                ('childcid1', models.CharField(max_length=16)),
                ('productid1', models.CharField(max_length=16)),
                ('longname1', models.CharField(max_length=100)),
                ('price1', models.FloatField(default=0)),
                ('marketprice1', models.FloatField(default=1)),
                ('img2', models.CharField(max_length=200)),
                ('childcid2', models.CharField(max_length=16)),
                ('productid2', models.CharField(max_length=16)),
                ('longname2', models.CharField(max_length=100)),
                ('price2', models.FloatField(default=0)),
                ('marketprice2', models.FloatField(default=1)),
                ('img3', models.CharField(max_length=200)),
                ('childcid3', models.CharField(max_length=16)),
                ('productid3', models.CharField(max_length=16)),
                ('longname3', models.CharField(max_length=100)),
                ('price3', models.FloatField(default=0)),
                ('marketprice3', models.FloatField(default=1)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
    ]
