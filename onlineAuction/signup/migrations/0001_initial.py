# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordRecovery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('email', models.EmailField(max_length=50)),
                ('link', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=50)),
                ('interests', models.CharField(default='Vehicle', max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visaNum', models.CharField(max_length=10)),
                ('expDate', models.DateTimeField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.UserDetail')),
            ],
        ),
    ]
