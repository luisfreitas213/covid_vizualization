# Generated by Django 2.2.5 on 2021-06-16 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cp_app', '0004_auto_20210616_0202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index_model',
            name='id',
        ),
        migrations.AlterField(
            model_name='index_model',
            name='index',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]