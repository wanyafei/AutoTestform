# Generated by Django 3.1.3 on 2020-12-14 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taste_user', '0015_auto_20201214_1434'),
        ('apitest', '0004_auto_20201214_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='taste_user.taste', verbose_name='报告对应的任务'),
        ),
    ]
