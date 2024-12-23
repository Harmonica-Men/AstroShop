# Generated by Django 4.2 on 2024-11-13 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_subscriber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_subscribed', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
    ]
