# Generated by Django 3.1.5 on 2021-02-10 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0004_auto_20210210_0850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='factured',
            new_name='paid',
        ),
    ]
