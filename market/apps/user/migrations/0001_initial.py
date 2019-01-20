# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-20 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='用户名,使用手机号')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('my_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='用户昵称')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别选择,默认保密')),
                ('my_birthday', models.DateField(blank=True, null=True, verbose_name='用户生日,默认为空')),
                ('school', models.CharField(blank=True, max_length=50, null=True, verbose_name='学校')),
                ('my_home', models.CharField(blank=True, max_length=50, null=True, verbose_name='用户详细地址位置')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='用户的故乡')),
                ('tel', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话号码')),
                ('is_delete', models.BooleanField(default=False)),
                ('add_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
            ],
        ),
    ]
