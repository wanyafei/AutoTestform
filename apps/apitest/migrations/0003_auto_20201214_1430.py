# Generated by Django 3.1.3 on 2020-12-14 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0002_report_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='plant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='apitest.plan', verbose_name='报告对应的计划'),
        ),
    ]
