# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitbot', '0005_auto_20170920_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='student',
            name='usc_email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
    ]