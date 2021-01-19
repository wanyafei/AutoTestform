# Generated by Django 3.1.3 on 2020-12-14 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_env', '0008_auto_20201213_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '有效'), (0, '失效')], default=1, verbose_name='环境状态'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '有效'), (0, '失效')], default=1, verbose_name='项目状态'),
        ),
    ]