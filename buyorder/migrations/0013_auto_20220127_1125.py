# Generated by Django 3.1.5 on 2022-01-27 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
        ('buyorder', '0012_buyorderitem_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='supplier.supplier'),
        ),
    ]