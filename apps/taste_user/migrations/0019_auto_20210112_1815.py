# Generated by Django 3.1.3 on 2021-01-12 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taste_user', '0018_auto_20210106_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=45),
        ),
    ]
