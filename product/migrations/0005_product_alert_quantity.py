# Generated by Django 3.1.5 on 2021-02-11 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20210207_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='alert_quantity',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
