# Generated by Django 3.1.5 on 2021-08-16 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='credit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
