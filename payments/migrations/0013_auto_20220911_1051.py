# Generated by Django 3.1.5 on 2022-09-11 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellorder', '0027_auto_20220510_1033'),
        ('payments', '0012_auto_20220622_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellorderpayment',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_items', to='sellorder.order'),
        ),
    ]
