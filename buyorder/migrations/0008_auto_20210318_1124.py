# Generated by Django 3.1.5 on 2021-03-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyorder', '0007_buyorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorder',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='buyorder',
            name='confirmed',
            field=models.BooleanField(default=True),
        ),
    ]