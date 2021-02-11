# Generated by Django 3.1.5 on 2021-02-10 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyorder', '0002_buyorder_debt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='debt',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
