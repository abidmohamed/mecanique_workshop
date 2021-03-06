# Generated by Django 3.0.6 on 2021-01-17 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('ref', models.CharField(max_length=250, null=True)),
                ('desc', models.CharField(max_length=250, null=True)),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
                ('buyprice', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('sellpricenormal', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.Category')),
                ('stock', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.Stock')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('name',),
            },
        ),
    ]
