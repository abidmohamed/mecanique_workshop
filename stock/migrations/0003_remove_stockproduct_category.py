# Generated by Django 3.1.5 on 2021-02-07 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_stockproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockproduct',
            name='category',
        ),
    ]
