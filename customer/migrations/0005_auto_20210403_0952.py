# Generated by Django 3.1.5 on 2021-04-03 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20210327_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='enterprise',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rc', models.CharField(max_length=250, null=True)),
                ('nif', models.CharField(max_length=250, null=True)),
                ('nis', models.CharField(max_length=250, null=True)),
                ('art', models.CharField(max_length=250, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='customer.customer')),
            ],
        ),
    ]
