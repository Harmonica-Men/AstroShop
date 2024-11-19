# Generated by Django 4.2 on 2024-11-19 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_order_customer_remove_order_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_company_name', models.CharField(max_length=100)),
                ('supplier_address1', models.CharField(max_length=200)),
                ('supplier_address2', models.CharField(blank=True, max_length=200, null=True)),
                ('supplier_city', models.CharField(max_length=200)),
                ('supplier_state', models.CharField(blank=True, max_length=200, null=True)),
                ('supplier_zipcode', models.CharField(blank=True, max_length=200, null=True)),
                ('supplier_country', models.CharField(max_length=200)),
                ('supplier_product', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
