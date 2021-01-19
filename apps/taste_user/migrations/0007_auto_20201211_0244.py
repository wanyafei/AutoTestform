# Generated by Django 3.1.3 on 2020-12-11 02:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taste_user', '0006_auto_20201210_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='taste',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='负责人'),
        ),
        migrations.AlterField(
            model_name='taste',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'RUNNING'), (0, 'STOP')], default=0, verbose_name='任务状态'),
        ),
    ]
