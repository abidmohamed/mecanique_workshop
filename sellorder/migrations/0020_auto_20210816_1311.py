# Generated by Django 3.1.5 on 2021-08-16 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0019_serviceitem_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceitem',
            name='charge',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
