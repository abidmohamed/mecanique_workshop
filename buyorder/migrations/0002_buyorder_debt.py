# Generated by Django 3.1.5 on 2021-02-09 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyorder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorder',
            name='debt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
