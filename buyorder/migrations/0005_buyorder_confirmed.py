# Generated by Django 3.1.5 on 2021-03-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyorder', '0004_auto_20210210_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorder',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]