# Generated by Django 3.1.5 on 2022-05-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0023_orderitem_buy_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='buy_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
