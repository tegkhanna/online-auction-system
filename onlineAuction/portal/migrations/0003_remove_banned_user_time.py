# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-09 06:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_banned_user_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banned_user',
            name='time',
        ),
    ]