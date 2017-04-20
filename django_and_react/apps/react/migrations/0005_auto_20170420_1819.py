# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 18:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20170420_1542'),
        ('react', '0004_task_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('win', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_members', to='react.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_group', to='login.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='groupmemeber',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupmemeber',
            name='user',
        ),
        migrations.DeleteModel(
            name='GroupMemeber',
        ),
    ]