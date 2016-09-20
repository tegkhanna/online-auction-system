# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 20:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import portal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signup', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='articleimage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='article_images/<built-in function id>.jpg', upload_to=portal.models.content_file_name)),
            ],
        ),
        migrations.CreateModel(
            name='articlereg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestart', models.DateTimeField()),
                ('articlename', models.CharField(max_length=40)),
                ('status', models.CharField(default='inactive', max_length=20)),
                ('category', models.CharField(max_length=40)),
                ('desc', models.CharField(max_length=150)),
                ('minbid', models.FloatField(default=0.0)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.UserDetail')),
            ],
        ),
        migrations.CreateModel(
            name='banned_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highestbid', models.FloatField(default=0.0)),
                ('articleid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.articlereg')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signup.UserDetail')),
            ],
        ),
        migrations.AddField(
            model_name='articleimage',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.articlereg'),
        ),
    ]