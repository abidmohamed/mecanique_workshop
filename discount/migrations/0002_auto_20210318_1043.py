# Generated by Django 3.1.5 on 2021-03-18 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0012_order_order_date'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellorder.order'),
        ),
    ]
