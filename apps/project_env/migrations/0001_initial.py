# Generated by Django 3.1.3 on 2020-12-08 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('prj_id', models.AutoField(primary_key=True, serialize=False, verbose_name='项目id')),
                ('prj_name', models.CharField(max_length=50, verbose_name='项目名称')),
                ('version', models.CharField(max_length=20, verbose_name='项目版本')),
                ('description', models.CharField(max_length=100, verbose_name='项目描述')),
                ('status', models.SmallIntegerField(choices=[(1, '有效'), (0, '失效')], default=1, verbose_name='项目状态')),
            ],
        ),
        migrations.CreateModel(
            name='Environment',
            fields=[
                ('env_id', models.AutoField(primary_key=True, serialize=False, verbose_name='环境id')),
                ('env_name', models.CharField(max_length=50, verbose_name='环境名字')),
                ('url', models.CharField(max_length=100, verbose_name='环境url')),
                ('description', models.CharField(max_length=100, verbose_name='环境描述')),
                ('status', models.SmallIntegerField(choices=[(1, '有效'), (0, '失效')], default=1, verbose_name='环境状态')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_env.project', verbose_name='项目名称')),
            ],
        ),
    ]
