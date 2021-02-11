# Generated by Django 3.1.5 on 2021-02-07 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicule', '0002_auto_20210207_1835'),
        ('sellorder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicule.vehicle'),
        ),
    ]
