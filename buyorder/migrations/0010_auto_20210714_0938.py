# Generated by Django 3.1.5 on 2021-07-14 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyorder', '0009_auto_20210320_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorderitem',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]