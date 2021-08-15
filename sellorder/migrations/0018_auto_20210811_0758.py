# Generated by Django 3.1.5 on 2021-08-11 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20210714_0932'),
        ('sellorder', '0017_auto_20210714_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='stockproduct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item', to='stock.stockproduct'),
        ),
    ]