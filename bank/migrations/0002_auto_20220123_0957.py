# Generated by Django 3.1.5 on 2022-01-23 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banktransaction',
            options={'ordering': ('trans_date',)},
        ),
    ]
