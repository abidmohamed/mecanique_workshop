# Generated by Django 3.1.5 on 2021-03-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0009_order_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_tva',
            field=models.PositiveIntegerField(default=0),
        ),
    ]