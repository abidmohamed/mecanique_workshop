# Generated by Django 3.1.5 on 2022-02-16 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caisse', '0004_auto_20220123_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='desc',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]