# Generated by Django 3.1.5 on 2021-03-18 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyorder', '0006_buyorder_order_tva'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorder',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
