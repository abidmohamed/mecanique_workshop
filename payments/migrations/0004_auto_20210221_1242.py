# Generated by Django 3.1.5 on 2021-02-21 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20210209_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorderpayment',
            name='pay_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sellorderpayment',
            name='pay_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
