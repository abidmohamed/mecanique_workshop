# Generated by Django 3.1.5 on 2021-04-29 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
        ('sellorder', '0015_order_timbre'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='sellorder.order')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_service', to='services.service')),
            ],
        ),
    ]