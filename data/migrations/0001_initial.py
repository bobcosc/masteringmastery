# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champion_id', models.CharField(max_length=25)),
                ('champion_name', models.CharField(max_length=60)),
                ('title', models.CharField(max_length=60)),
                ('image_full', models.CharField(max_length=25)),
                ('image_sprite', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summoner_id', models.CharField(max_length=25)),
                ('summoner_name', models.CharField(max_length=60)),
                ('region', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerChampionMastery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(blank=True, null=True)),
                ('champion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data.Champion')),
                ('summoner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='data.Player')),
            ],
        ),
    ]