# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitbot', '0006_auto_20170920_2037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commit',
            name='from_bot',
        ),
        migrations.RemoveField(
            model_name='commit',
            name='id',
        ),
        migrations.RemoveField(
            model_name='repo',
            name='id',
        ),
        migrations.AlterField(
            model_name='commit',
            name='sha',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='repo',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
