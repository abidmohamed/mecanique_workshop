# Generated by Django 3.1.5 on 2021-03-18 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0011_order_discount_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
