# Generated by Django 4.2 on 2024-10-30 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_paymentlog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentLog',
        ),
    ]
