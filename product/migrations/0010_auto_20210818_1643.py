# Generated by Django 3.1.5 on 2021-08-18 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20210811_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ref',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
