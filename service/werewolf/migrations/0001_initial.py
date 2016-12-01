# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-01 09:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameId', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]