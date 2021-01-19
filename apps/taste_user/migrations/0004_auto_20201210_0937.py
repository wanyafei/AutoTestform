# Generated by Django 3.1.3 on 2020-12-10 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taste_user', '0003_auto_20201210_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='project',
        ),
        migrations.AlterField(
            model_name='taste',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'STOP'), (1, 'RUNNING')], default=0, verbose_name='任务状态'),
        ),
    ]